#!/usr/bin/env python

import numpy as np
import tensorflow as tf
import gym
from dynamics import NNDynamicsModel
from controllers import MPCcontroller, RandomController
from cost_functions import laika_cost_fn, trajectory_cost_fn
import time
import logz
import os
import copy
import matplotlib.pyplot as plt
from state_callback import state_callback

import rospy
from Laika_ROS.msg import LaikaCommand, LaikaState, LaikaStateArray, LaikaAction

# curr_state = np.zeros(140) #number also hardcoded in dynamic and controller files

# def reset(state_cb,pub_cmd,rate):
#     cmd_msg = LaikaCommand()
#     cmd_msg.header.stamp = rospy.Time.now()
#     cmd_msg.cmd = 'reset'
#
#     pub_cmd.publish(cmd_msg)
#
#     state_cb.threading_cond.acquire()
#
#     while not state_cb.state_update:
#         print("In reset while loop")
#         state_cb.threading_cond.wait()
#
#     print("Out of while loop")
#     obs = state_cb.get_curr_state()
#
#     state_cb.threading_cond.release()
#
#     return obs
#
# def step(action,state_cb,pub_act,pub_cmd,rate):
#     # tmp = curr_state
#     act_msg = LaikaAction()
#     cmd_msg = LaikaCommand()
#     act_msg.header.stamp = rospy.Time.now()
#     act_msg.actions = action
#     cmd_msg.header.stamp = rospy.Time.now()
#     cmd_msg.cmd = 'step'
#
#     pub_act.publish(act_msg)
#     pub_cmd.publish(cmd_msg)
#
#     state_cb.threading_cond.acquire()
#
#     while not state_cb.state_update:
#         print("In step while loop")
#         state_cb.threading_cond.wait()
#
#     ob_tp1 = state_cb.get_curr_state()
#
#     state_cb.threading_cond.release()
#
#     done = 0
#
#     return ob_tp1,done

# def state_callback(msg):
#     state = []
#     for i in range(len(msg.states)):
#         state = state+[msg.states[i].position.x,msg.states[i].position.y,msg.states[i].position.z] \
#             +[msg.states[i].orientation.x,msg.states[i].orientation.y,msg.states[i].orientation.z] \
#             +[msg.states[i].lin_vel.x,msg.states[i].lin_vel.y,msg.states[i].lin_vel.z] \
#             +[msg.states[i].ang_vel.x,msg.states[i].ang_vel.y,msg.states[i].ang_vel.z]
#     # print(msg.cable_rl)
#     state = state+list(msg.cable_rl)
#     global curr_state
#     curr_state = np.array(state)

    # rospy.loginfo(msg)

def sample(state_cb,pub_cmd,pub_act,rate,controller,
           num_paths=10,
           horizon=1000,
           render=False,
           verbose=False):
    """
        Write a sampler function which takes in an environment, a controller (either random or the MPC controller),
        and returns rollouts by running on the env.
        Each path can have elements for observations, next_observations, rewards, returns, actions, etc.
    """
    print('Sampling trajectories...')

    paths = []

    for i in range(num_paths):
        obs_t, obs_tp1, acs_t, rews_t = [], [], [], []
        ob_t = state_cb.reset(pub_act,pub_cmd)
        # print(ob_t)
        rate.sleep()
        for _ in range(horizon):
            # Calculate action and step the environment
            ac_t = controller.get_action(ob_t)
            ob_tp1, _ = state_cb.step(ac_t,pub_act,pub_cmd)
            rew_t = 0
            for i in range(9):
                # rew_t += ob_tp1[i*12]-ob_t[i*12]
                rew_t += ob_tp1[i*12]/9

            # Append to vectors
            obs_t.append(ob_t)
            obs_tp1.append(ob_tp1)
            acs_t.append(ac_t)
            rews_t.append(rew_t)

            # Move time forward
            ob_t = ob_tp1

            rate.sleep()

        path = {"observations":np.array(obs_t),
                "next_observations":np.array(obs_tp1),
                "actions":np.array(acs_t),
                "rewards":np.array(rews_t)}
        paths.append(path)
        print(len(paths))
        print('Observation dimension: ',path['observations'].shape)
        print('Action dimension: ',path['actions'].shape)
    return paths

# Utility to compute cost a path for a given cost function
def path_cost(cost_fn, path):
    return trajectory_cost_fn(cost_fn, path['observations'], path['actions'], path['next_observations'])

def paths_to_array(paths):
    print('Converting paths to dataset...')

    for i in range(len(paths)):
        if i == 0:
            obs_t = paths[i]['observations']
            obs_tp1 = paths[i]['next_observations']
            acs_t = paths[i]['actions']
            rew_t = paths[i]['rewards']
        else:
            obs_t = np.append(obs_t,paths[i]['observations'],axis=0)
            obs_tp1 = np.append(obs_tp1,paths[i]['next_observations'],axis=0)
            acs_t = np.append(acs_t,paths[i]['actions'],axis=0)
            rew_t = np.append(rew_t,paths[i]['rewards'],axis=0)

    n_data = obs_t.shape[0]
    data = {'obs_t':obs_t, 'obs_tp1':obs_tp1, 'acs_t':acs_t, 'rew_t':rew_t}
    print('Dataset built with %i datapoints' % n_data)
    return data

def compute_normalization(data):
    """
    Write a function to take in a dataset and compute the means, and stds.
    Return 6 elements: mean of s_t, std of s_t, mean of (s_t+1 - s_t), std of (s_t+1 - s_t), mean of actions, std of actions
    """
    print('Computing normalization statistics...')
    obs_t = data['obs_t']
    obs_tp1 = data['obs_tp1']
    acs_t = data['acs_t']
    deltas = obs_tp1-obs_t

    mean_obs = np.mean(obs_t,axis=0)
    std_obs = np.std(obs_t,axis=0)
    mean_deltas = np.mean(deltas,axis=0)
    std_deltas = np.std(deltas,axis=0)
    mean_action = np.mean(acs_t,axis=0)
    std_action = np.std(acs_t,axis=0)

    normalization = {'mean_obs':mean_obs, 'std_obs':std_obs,
                    'mean_deltas':mean_deltas, 'std_deltas':std_deltas,
                    'mean_acs':mean_action, 'std_acs':std_action}
    return normalization

def plot_comparison(dyn_model, state_cb, pub_act, pub_cmd, rate):
    """
    Write a function to generate plots comparing the behavior of the model predictions for each element of the state to the actual ground truth, using randomly sampled actions.
    """
    print('Plotting nn dynamics results')
    rand_cont = RandomController()
    s = state_cb.reset(pub_act,pub_cmd)
    env_state_traj = s
    model_state_traj = s
    steps = 100
    for i in range(steps):
        a = rand_cont.get_action(None)
        # Step environment
        env_s, _ = state_cb.step(a,pub_act,pub_cmd)
        env_state_traj = np.vstack((env_state_traj,env_s))
        # Step model
        if i == 0:
            model_s = dyn_model.predict(model_state_traj,a)
        else:
            model_s = dyn_model.predict(model_state_traj[i,:],a)
        model_state_traj = np.vstack((model_state_traj,model_s))

    body = 10
    # for i in range(body*12,(body+1)*12):
    for i in [0,1,2,3,4,5,6,7,8,9,10,11,108,109,110]:
        plt.figure()
        env_state = plt.plot(np.arange(steps+1),env_state_traj[:,i].reshape((steps+1)),label='env state')
        model_state = plt.plot(np.arange(steps+1),model_state_traj[:,i].reshape((steps+1)),label='model state')
        state = i%12
        if state == 0:
            plt.title('Body '+str(body)+', x position')
        elif state == 1:
            plt.title('Body '+str(body)+', y position')
        elif state == 2:
            plt.title('Body '+str(body)+', z position')
        elif state == 3:
            plt.title('Body '+str(body)+', x angle')
        elif state == 4:
            plt.title('Body '+str(body)+', y angle')
        elif state == 5:
            plt.title('Body '+str(body)+', z angle')
        elif state == 6:
            plt.title('Body '+str(body)+', x velocty')
        elif state == 7:
            plt.title('Body '+str(body)+', y velocity')
        elif state == 8:
            plt.title('Body '+str(body)+', z velocity')
        elif state == 9:
            plt.title('Body '+str(body)+', x angular velocity')
        elif state == 10:
            plt.title('Body '+str(body)+', y angular velocity')
        elif state == 11:
            plt.title('Body '+str(body)+', z angular velocity')
        plt.legend()
        plt.draw()
    plt.show()

def train(state_cb,pub_cmd,pub_act,rate,
         cost_fn,
         logdir=None,
         render=False,
         learning_rate=1e-3,
         onpol_iters=10,
         dynamics_iters=60,
         batch_size=512,
         num_paths_random=10,
         num_paths_onpol=10,
         num_simulated_paths=10000,
         env_horizon=1000,
         mpc_horizon=15,
         n_layers=2,
         size=500,
         activation=tf.nn.relu,
         output_activation=None
         ):

    """

    Arguments:

    onpol_iters                 Number of iterations of onpolicy aggregation for the loop to run.

    dynamics_iters              Number of iterations of training for the dynamics model
    |_                          which happen per iteration of the aggregation loop.

    batch_size                  Batch size for dynamics training.

    num_paths_random            Number of paths/trajectories/rollouts generated
    |                           by a random agent. We use these to train our
    |_                          initial dynamics model.

    num_paths_onpol             Number of paths to collect at each iteration of
    |_                          aggregation, using the Model Predictive Control policy.

    num_simulated_paths         How many fictitious rollouts the MPC policy
    |                           should generate each time it is asked for an
    |_                          action.

    env_horizon                 Number of timesteps in each path.

    mpc_horizon                 The MPC policy generates actions by imagining
    |                           fictitious rollouts, and picking the first action
    |                           of the best fictitious rollout. This argument is
    |                           how many timesteps should be in each fictitious
    |_                          rollout.

    n_layers/size/activations   Neural network architecture arguments.

    """

    logz.configure_output_dir(logdir)

    #========================================================
    #
    # First, we need a lot of data generated by a random
    # agent, with which we'll begin to train our dynamics
    # model.

    rand_controller = RandomController()
    paths = sample(state_cb,pub_cmd,pub_act,rate,rand_controller,num_paths_random,env_horizon,render)
    data = paths_to_array(paths)

    #========================================================
    #
    # The random data will be used to get statistics (mean
    # and std) for the observations, actions, and deltas
    # (where deltas are o_{t+1} - o_t). These will be used
    # for normalizing inputs and denormalizing outputs
    # from the dynamics network.
    #
    normalization = compute_normalization(data)

    #========================================================
    #
    # Build dynamics model and MPC controllers.
    #
    sess = tf.Session()

    dyn_model = NNDynamicsModel(n_layers=n_layers,
                                size=size,
                                activation=activation,
                                output_activation=output_activation,
                                normalization=normalization,
                                batch_size=batch_size,
                                iterations=dynamics_iters,
                                learning_rate=learning_rate,
                                sess=sess)

    mpc_controller = MPCcontroller(dyn_model=dyn_model,
                                   horizon=mpc_horizon,
                                   cost_fn=cost_fn,
                                   num_simulated_paths=num_simulated_paths)

    #========================================================
    #
    # Tensorflow session building.
    #
    sess.__enter__()
    tf.global_variables_initializer().run()

    #========================================================
    #
    # Take multiple iterations of onpolicy aggregation at each iteration refitting the dynamics model to current dataset and then taking onpolicy samples and aggregating to the dataset.
    # Note: You don't need to use a mixing ratio in this assignment for new and old data as described in https://arxiv.org/abs/1708.02596
    #
    for itr in range(onpol_iters):
        # Fit dynamics model
        print('Training dynamics model...')
        dyn_model.fit(data)
        plot_comparison(dyn_model,state_cb,pub_act,pub_cmd,rate)
        mpc_controller.dyn_model = dyn_model
        costs = []
        returns = []
        # Do MPC
        for i in range(num_paths_onpol):
            print('On policy path: %i' % i)
            obs_t, obs_tp1, acs_t, rews_t = [], [], [], []
            s_t = state_cb.reset(pub_act,pub_cmd)
            total_return = 0

            for j in range(env_horizon):
                # print('Timestep: %i, Return: %g' % (j,total_return))
                a_t = mpc_controller.get_action(s_t)
                s_tp1,_ = state_cb.step(a_t,pub_act,pub_cmd)
                r_t = 0
                for i in range(9):
                    r_t += s_tp1[i*12]-s_t[i*12]
                total_return += r_t

                if render:
                    env.render()
                    time.sleep(0.05)

                obs_t.append(s_t)
                obs_tp1.append(s_tp1)
                acs_t.append(a_t)
                rews_t.append(r_t)

                s_t = s_tp1

            path = {"observations":np.array(obs_t),
                    "next_observations":np.array(obs_tp1),
                    "actions":np.array(acs_t),
                    "rewards":np.array(rews_t)}
            total_cost = path_cost(cost_fn,path)

            paths.append(path)
            returns.append(total_return)
            costs.append(total_cost)
            print('Total cost: %g, Total reward: %g' % (total_cost,total_return))

        data = paths_to_array(paths)
        normalization = compute_normalization(data)
        # Set new normalization statistics for dynamics model
        dyn_model.normalization = normalization

        # LOGGING
        # Statistics for performance of MPC policy using
        # our learned dynamics model
        logz.log_tabular('Iteration', itr)
        # In terms of cost function which your MPC controller uses to plan
        logz.log_tabular('AverageCost', np.mean(costs))
        logz.log_tabular('StdCost', np.std(costs))
        logz.log_tabular('MinimumCost', np.min(costs))
        logz.log_tabular('MaximumCost', np.max(costs))
        # In terms of true environment reward of your rolled out trajectory using the MPC controller
        logz.log_tabular('AverageReturn', np.mean(returns))
        logz.log_tabular('StdReturn', np.std(returns))
        logz.log_tabular('MinimumReturn', np.min(returns))
        logz.log_tabular('MaximumReturn', np.max(returns))

        logz.dump_tabular()

def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_name', type=str, default='HalfCheetah-v1')
    # Experiment meta-params
    parser.add_argument('--exp_name', type=str, default='mb_mpc')
    parser.add_argument('--seed', type=int, default=3)
    parser.add_argument('--render', action='store_true')
    # Training args
    parser.add_argument('--learning_rate', '-lr', type=float, default=1e-4)
    parser.add_argument('--onpol_iters', '-n', type=int, default=10)
    parser.add_argument('--dyn_iters', '-nd', type=int, default=50)
    parser.add_argument('--batch_size', '-b', type=int, default=512)
    # Data collection
    parser.add_argument('--random_paths', '-r', type=int, default=10)
    parser.add_argument('--onpol_paths', '-d', type=int, default=5)
    parser.add_argument('--simulated_paths', '-sp', type=int, default=1000)
    parser.add_argument('--ep_len', '-ep', type=int, default=2000)
    # Neural network architecture args
    parser.add_argument('--n_layers', '-l', type=int, default=2)
    parser.add_argument('--size', '-s', type=int, default=500)
    # MPC Controller
    parser.add_argument('--mpc_horizon', '-m', type=int, default=10)
    args = parser.parse_args()

    # Set seed
    np.random.seed(args.seed)
    tf.set_random_seed(args.seed)

    # Make data directory if it does not already exist
    if not(os.path.exists('data')):
        os.makedirs('data')
    logdir = args.exp_name + '_' + args.env_name + '_' + time.strftime("%d-%m-%Y_%H-%M-%S")
    logdir = os.path.join('data', logdir)
    if not(os.path.exists(logdir)):
        os.makedirs(logdir)

    # Initialize ros
    rospy.init_node('laika_control', anonymous=True)
    rate = rospy.Rate(100) # 10hz

    # Initialize publishers and subscribers
    pub_cmd = rospy.Publisher('cmd', LaikaCommand, queue_size=1)
    pub_act = rospy.Publisher('action', LaikaAction, queue_size=1)

    state_cb = state_callback()
    sub_state = rospy.Subscriber('state', LaikaStateArray, callback=state_cb.handle_state_msg, queue_size=1)

    cost_fn = laika_cost_fn

    train(state_cb,pub_cmd,pub_act,rate,cost_fn=cost_fn,
                 logdir=logdir,
                 render=args.render,
                 learning_rate=args.learning_rate,
                 onpol_iters=args.onpol_iters,
                 dynamics_iters=args.dyn_iters,
                 batch_size=args.batch_size,
                 num_paths_random=args.random_paths,
                 num_paths_onpol=args.onpol_paths,
                 num_simulated_paths=args.simulated_paths,
                 env_horizon=args.ep_len,
                 mpc_horizon=args.mpc_horizon,
                 n_layers = args.n_layers,
                 size=args.size,
                 activation=tf.nn.relu,
                 output_activation=None)

if __name__ == "__main__":
    main()
