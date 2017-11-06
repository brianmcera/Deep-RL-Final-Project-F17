#!/usr/bin/env python

import rospy
from std_msgs.msg import String, UInt32
from gps_agent_pkg.msg import LaikaCommand

def state_callback(msg):
    rospy.loginfo(rospy.get_caller_id() + 'State: %i' %(msg.data))

def init_node():
    # Initialize node
    rospy.init_node('laika_control', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # Initialize publishers and subscribers
    pub = rospy.Publisher('cmd', String, queue_size=1)
    sub = rospy.Subscriber('state', UInt32, state_callback)

    return pub, sub

if __name__ == '__main__':
    pub, sub = init_node()
    counter = 0
    control_msg = String()
    # state_msg = UInt32()

    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        if counter % 100 == 0:
            control_msg.data = 'reset'
        else:
            control_msg.data = 'step'
        pub.publish(control_msg)
        rospy.loginfo(control_msg)

        counter += 1

        rate.sleep()
