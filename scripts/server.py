#!/usr/bin/env python

import rospy
from capra_controlpanel.msg import *
from communication.communication import Communication

def run():
    seq = 0
    comm = Communication("/dev/pts/14", 19200)
    pub = rospy.Publisher("chatter", State, queue_size=10)
    rospy.init_node('capra_controlpanel')
    r = rospy.Rate(1)
    print "Starting..."
    while not rospy.is_shutdown():
        comm.start()
    
        state = State()
        state.header.seq = seq
        seq+=1
        state.header.stamp = rospy.Time.now()
        state.name = "test"
        state.state = False
        rospy.loginfo(state)
        pub.publish(state)
        r.sleep()

if __name__ == "__main__":
    try:
        run()
    except rospy.ROSInterruptException: pass
