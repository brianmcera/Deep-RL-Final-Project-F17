import numpy as np
import threading
from Laika_ROS.msg import LaikaCommand, LaikaState, LaikaStateArray, LaikaAction
import rospy
import time

class state_callback:
    def __init__(self):
        self.curr_state = np.zeros(140)
        self.prev_state = np.zeros(140)
        self.prev2_state = np.zeros(140)
        self.state_update = False
        self.last_state_msg_time = 0
        self.threading_cond = threading.Condition()

        # self.reset()

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

    def reset(self,pub_act,pub_cmd):
        # print('Resetting')
        cmd_msg = LaikaCommand()
        cmd_msg.header.stamp = rospy.Time.now()
        cmd_msg.cmd = 'reset'

        # print("Number of connections: ",pub_cmd.get_num_connections())
        while pub_cmd.get_num_connections() == 0:
            pass
        # print(cmd_msg)
        pub_cmd.publish(cmd_msg)

        # time.sleep(0.5)
        self.threading_cond.acquire()

        while not self.state_update:
            # print("Waiting for new state reading")
            self.threading_cond.wait()

        # print("Out of while loop")
        obs = self.get_curr_state()

        self.threading_cond.release()

        return obs

    def step(self,action,pub_act,pub_cmd):
        # print('Stepping')
        # tmp = curr_state
        act_msg = LaikaAction()
        cmd_msg = LaikaCommand()
        act_msg.header.stamp = rospy.Time.now()
        act_msg.actions = action
        cmd_msg.header.stamp = rospy.Time.now()
        cmd_msg.cmd = 'step'

        pub_act.publish(act_msg)
        pub_cmd.publish(cmd_msg)

        while (pub_cmd.get_num_connections() == 0) or (pub_act.get_num_connections() == 0):
            pass

        self.threading_cond.acquire()

        while not self.state_update:
            # print("Waiting for new state reading")
            self.threading_cond.wait()

        ob_tp1 = self.get_curr_state()

        self.threading_cond.release()

        done = 0

        return ob_tp1,done
