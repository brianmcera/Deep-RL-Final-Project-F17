#!/usr/bin/env python

import rospy
from std_msgs.msg import String, UInt32
from gps_agent_pkg.msg import LaikaCommand, LaikaState, LaikaStateArray, LaikaAction
import numpy as np

def state_callback(msg):
    rospy.loginfo(msg)

def init_node():
    # Initialize node
    rospy.init_node('laika_control', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # Initialize publishers and subscribers
    pub_cmd = rospy.Publisher('cmd', LaikaCommand, queue_size=1)
    pub_act = rospy.Publisher('action', LaikaAction, queue_size=1)
    sub = rospy.Subscriber('state', LaikaStateArray, state_callback)

    return pub_cmd, pub_act, sub

if __name__ == '__main__':
    pub_cmd, pub_act, sub = init_node()
    counter = 0
    cmd_msg = LaikaCommand()
    act_msg = LaikaAction()
    # state_msg = UInt32()

    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        cmd_msg.header.seq = counter
        cmd_msg.header.stamp = rospy.Time.now()
        act_msg.header.seq = counter
        act_msg.header.stamp = rospy.Time.now()
        act_msg.actions = np.random.uniform(5,15,44)
        if counter % 100 == 0:
            cmd_msg.cmd = 'reset'
        else:
            cmd_msg.cmd = 'step'
        pub_cmd.publish(cmd_msg)
        rospy.loginfo(cmd_msg)
        pub_act.publish(act_msg)
        rospy.loginfo(act_msg)

        counter += 1

        rate.sleep()
