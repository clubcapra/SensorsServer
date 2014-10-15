#!/usr/bin/env python

import rospy
from capra_controlpanel.msg import *
from capra_controlpanel.srv import *
from communication.communication import Communication

def handle_controlpanel_get(req):
    print "got call get with param " + req.name + ". returning 0"
    return 0

def handle_controlpanel_set(req):
    print "got call set with param " + req.name + " to " + str(req.state) + ". returning True"
    return True

def capra_controlpanel_server():
    rospy.init_node('capra_controlpanel')
    s_get = rospy.Service('capra_controlpanel/get', Get, handle_controlpanel_get)
    s_set = rospy.Service('capra_controlpanel/set', Set, handle_controlpanel_set)
#    seq = 0
#    comm = Communication("/dev/pts/14", 19200)
#    pub = rospy.Publisher("chatter", State, queue_size=10)
#    r = rospy.Rate(1)
    print "Starting..."
#    while not rospy.is_shutdown():
#        comm.start()
#    
#        state = State()
#        state.header.seq = seq
#        seq+=1
#        state.header.stamp = rospy.Time.now()
#        state.name = "test"
#        state.state = False
#        rospy.loginfo(state)
#        pub.publish(state)
#        r.sleep()
    rospy.spin()

if __name__ == "__main__":
    try:
        capra_controlpanel_server()
    except rospy.ROSInterruptException: pass
