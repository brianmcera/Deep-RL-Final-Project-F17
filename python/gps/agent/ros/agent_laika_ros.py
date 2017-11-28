""" This file defines an agent for the NTRT Laika Environment. """
import copy
import time
import numpy as np
import threading
import rospy

from gps.agent.agent import Agent
from gps.agent.config import AGENT_LAIKA_ROS
from gps.agent.agent_utils import generate_noise, setup
from Laika_ROS.msg import LaikaState, LaikaStateArray, LaikaAction, LaikaCommand
from gps.proto.gps_pb2 import BODY_POSITIONS, BODY_VELOCITIES, CABLE_RL, ACTION
from gps.sample.sample import Sample
try:
    from gps.algorithm.policy.tf_policy import TfPolicy
except ImportError:  # user does not have tf installed.
    TfPolicy = None

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class AgentLaikaROS(Agent):
    """
    All communication between the algorithms and ROS is done through
    this class.
    """
    def __init__(self, hyperparams, init_node=True):
        """
        Initialize agent.
        Args:
            hyperparams: Dictionary of hyperparameters.
            init_node: Whether or not to initialize a new ROS node.
        """
        config = copy.deepcopy(AGENT_LAIKA_ROS)
        config.update(hyperparams)
        Agent.__init__(self, config)

        if init_node:
            rospy.init_node('gps_Laika_agent_ros_node')
        self.pub_cmd = rospy.Publisher('cmd', LaikaCommand, queue_size=1)
        self.pub_act = rospy.Publisher('action', LaikaAction, queue_size=1)
        self.sub_state = rospy.Subscriber('state', LaikaStateArray, callback=self.handle_state_msg, queue_size=1)

        self._seq_id = 0  # Used for setting seq in ROS commands.

        conditions = self._hyperparams['conditions']

        self.x0 = []
        self._hyperparams['x0'] = setup(self._hyperparams['x0'],
                                             conditions)
        self.x0 = self._hyperparams['x0']

        r = rospy.Rate(100)
        r.sleep()

        self.curr_state = np.zeros(140) #hardcoded dimensions for now, change later
        self.prev_state = np.zeros(140)
        self.prev2_state = np.zeros(140)
        self.state_update = False
        self.last_state_msg_time = 0
        self.threading_cond = threading.Condition()


    def reset(self, condition, policy=None):
        """
        Reset the agent for a particular experiment condition.
        Args:
            condition: An index into hyperparams['reset_conditions'].
        """
        cmd_msg = LaikaCommand()
        cmd_msg.header.stamp = rospy.Time.now()

        reset_with_action = self._hyperparams['reset_with_rand_action']
        # print("Number of connections: ",pub_cmd.get_num_connections())
        while self.pub_cmd.get_num_connections() == 0:
            pass
        # print(cmd_msg)

        if(reset_with_action):
            print('Simulation reset with randomized action')
            cmd_msg.cmd = 'reset_w_action'
            self.pub_cmd.publish(cmd_msg)
            act_msg = LaikaAction()
            act_msg.header.stamp = rospy.Time.now()
            # act_msg.actions = (np.random.uniform(size=self.dU)-0.5)*10
            act_msg.actions = (np.random.uniform(size=self.dU)-0.5)*40
            self.pub_act.publish(act_msg)
        else:
            print('Simulation reset')
            cmd_msg.cmd = 'reset'
            self.pub_cmd.publish(cmd_msg)

        # time.sleep(0.5)
        self.threading_cond.acquire()

        while not self.state_update:
            # print("Waiting for new state reading")
            self.threading_cond.wait()

        # print("Out of while loop")
        obs = self.get_curr_state()

        self.threading_cond.release()

        return obs

    def step(self,action):
        # print('Stepping')
        # tmp = curr_state

        act_msg = LaikaAction()
        cmd_msg = LaikaCommand()
        act_msg.header.stamp = rospy.Time.now()
        act_msg.actions = action
        cmd_msg.header.stamp = rospy.Time.now()
        cmd_msg.cmd = 'step'

        self.pub_act.publish(act_msg)
        self.pub_cmd.publish(cmd_msg)

        while (self.pub_cmd.get_num_connections() == 0) or (self.pub_act.get_num_connections() == 0):
            #print('checking for connections')
            pass

        self.threading_cond.acquire()

        while not self.state_update:
            # print("Waiting for new state reading")
            self.threading_cond.wait()

        ob_tp1 = self.get_curr_state()

        self.threading_cond.release()

        done = 0
        return ob_tp1,done


    def handle_state_msg(self, msg):
        self.threading_cond.acquire()
        # print("Reading new state")

        state = []
        for i in range(len(msg.states)):
            state = state+[msg.states[i].position.x,msg.states[i].position.y,msg.states[i].position.z] \
                +[msg.states[i].orientation.x,msg.states[i].orientation.y,msg.states[i].orientation.z] \
                +[msg.states[i].lin_vel.x,msg.states[i].lin_vel.y,msg.states[i].lin_vel.z] \
                +[msg.states[i].ang_vel.x,msg.states[i].ang_vel.y,msg.states[i].ang_vel.z]
        # print(msg.cable_rl)
        state = state+list(msg.cable_rl)
        curr_state = np.array(state)

        self.prev2_state = self.prev_state
        self.prev_state = self.curr_state
        self.curr_state = curr_state
        # self.last_state_msg_time = msg.header.stamp.nsecs

        self.state_update = True

        # print("Got to notify")
        self.threading_cond.notify()
        self.threading_cond.release()

        # Plot positions
        # fig = plt.figure(1)
        # ax = fig.gca(projection='3d')
        #
        # plt.cla()
        # positions = []
        # for i in range(18):
        #     if i%2 == 0:
        #         positions.append(curr_state[i*6:(i+1)*6])
        #         # positions = curr_state[i*6:(i+1)*6]
        #         # ax.scatter(positions[0],-positions[2],positions[1])
        # positions = np.array(positions)
        # body = positions[0:5,:]
        # front_legs = np.vstack((positions[7,:],positions[0,:],positions[8,:]))
        # back_legs = np.vstack((positions[5,:],positions[4,:],positions[6,:]))
        #
        # ax.plot(body[:,0],-body[:,2],body[:,1],'-bo')
        # ax.plot(front_legs[:,0],-front_legs[:,2],front_legs[:,1],'-ro')
        # ax.plot(back_legs[:,0],-back_legs[:,2],back_legs[:,1],'-go')
        #
        # ax.set_zlim(0,40)
        # plt.draw()

    def get_curr_state(self):
        self.state_update = False
        return self.curr_state


    def sample(self, policy, condition, verbose=True, save=True, noisy=True):
        """
        Reset and execute a policy and collect a sample.
        Args:
            policy: A Policy object.
            condition: Which condition setup to run.
            verbose: Unused for this agent.
            save: Whether or not to store the trial into the samples.
            noisy: Whether or not to use noise during sampling.
        Returns:
            sample: A Sample object.
        """
        # print('agent_laika_ros/sample: getting new sample')
        ob = self.reset(condition)
        # print(ob)
        ob_parsed = self.form_struct_ob(ob)
        # print('Make new sample')
        new_sample = self._init_sample(ob_parsed)
        U = np.zeros([self.T, self.dU])
        # Generate noise.
        if noisy:
            noise = generate_noise(self.T, self.dU, self._hyperparams)
        else:
            noise = np.zeros((self.T, self.dU))

        # Execute trial.
        for t in range(self.T):
            X_t = new_sample.get_X(t=t)
            obs_t = new_sample.get_obs(t=t)
            # print('Create new action')
            U[t, :] = policy.act(X_t, obs_t, t, noise[t, :])
            if (t+1) < self.T:
                for _ in range(self._hyperparams['substeps']):
                    # print('Agent_laika_ros/stepping call')
                    new_X,done = self.step(U[t,:])
                    new_X_parsed = self.form_struct_ob(new_X)
                self._set_sample(new_sample, new_X_parsed, t)

        new_sample.set(ACTION,U)
        if save:
            self._samples[condition].append(new_sample)
        return new_sample


    def _init_sample(self, X):
        """
        Construct a new sample and fill in the first time step.
        """
        sample = Sample(self)
        self._set_sample(sample, X, -1)
        return sample


    def _set_sample(self, sample, X, t):
        for sensor in X.keys():
            sample.set(sensor, np.array(X[sensor]), t=t+1)


    def form_struct_ob(self,ob):
        positions = [ob[i*6:(i+1)*6] for i in range(18) if i%2==0]
        velocities = [ob[i*6:(i+1)*6] for i in range(18) if i%2==1]
        state = {BODY_POSITIONS: np.array(positions).flatten(),
                 BODY_VELOCITIES: np.array(velocities).flatten(),
                 CABLE_RL : ob[108:]} #hardcoded for now, change later
        return state
