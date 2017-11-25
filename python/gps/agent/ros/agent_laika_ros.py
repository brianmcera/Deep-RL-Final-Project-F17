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

try:
    from gps.algorithm.policy.tf_policy import TfPolicy
except ImportError:  # user does not have tf installed.
    TfPolicy = None

    

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
        for field in ('x0', 'reset_conditions'):
            self._hyperparams[field] = setup(self._hyperparams[field],
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


    def reset(self, condition):
        """
        Reset the agent for a particular experiment condition.
        Args:
            condition: An index into hyperparams['reset_conditions'].
        """
        cmd_msg = LaikaCommand()
        cmd_msg.header.stamp = rospy.Time.now()
        cmd_msg.cmd = 'reset'

        # print("Number of connections: ",pub_cmd.get_num_connections())
        while self.pub_cmd.get_num_connections() == 0:
            pass
        # print(cmd_msg)
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

        ob = self.reset(condition)
        ob_parsed = form_struct_ob(ob)
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
            U[t, :] = policy.act(X_t, obs_t, t, noise[t, :])
            if (t+1) < self.T:
                for _ in range(self._hyperparams['substeps']):
                    new_X = self.step(U[t,:])
                    new_X_parsed = form_struct_ob(new_X)
                    self._set_sample(new_sample, new_X_parsed, t)
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
        state = {BODY_STATES : ob[0:108],
                 CABLE_RL : ob[108:]} #hardcoded for now, change later
        return state



        
