#!/usr/bin/env python

import rospy
from capra_controlpanel.msg import *
from capra_controlpanel.srv import *

import comm.communication
from comm.communication import Communication

import time

def handle_controlpanel_set(req):
    rospy.logdebug("got call SET with param " + req.name + " and " + str(req.state))
    
    cmd = "ON"
    if req.state is False:
        cmd = "OFF"
    
    status, reply = comm.communication.instance.send_command("SET " + req.name + " " + cmd)
    
    if not status:
        reply = "communication error"
    
    if reply is None:
        reply = ""
    else:
        rospy.logdebug("handle_controlpanel_set: sending response to client: '" + reply + "'")

    return True
    
class ControlPanelServer:

    def __init__(self):
        rospy.init_node('capra_controlpanel')
        rospy.set_param
        pub_robot_buttons = rospy.Publisher("~buttons", RobotButtons, queue_size=10)
        pub_robot_analog_values = rospy.Publisher("~analog_values", RobotAnalogValues, queue_size=10)

        ids = rospy.get_param('~sensor_ids')
        s_set = rospy.Service('capra_controlpanel/set', Set, handle_controlpanel_set)

        comm.communication.instance = Communication(ids, rospy.get_param('~serial_port'), 19200)
        success = comm.communication.instance.start()
        if not success:
            rospy.logfatal("Unable to start controlpanel node")
            sys.exit()
        else:
            rospy.loginfo("Controlpanel connected to serial port")
        comm.communication.stop_all = False

        rate = rospy.get_param('~publish_rate')
        r = rospy.Rate(rate)
        serial_wait = float(rospy.get_param('~serial_wait'))

        rospy.loginfo("Starting controlpanel. Serial polling slep: " + str(serial_wait) + " . Message rate(hz): " + str(r))
        while not rospy.is_shutdown():

            #Read button data
            robot_buttons = RobotButtons()
            fields = robot_buttons.__slots__
            for field in fields:
                status, reply = comm.communication.instance.send_command("GET " + field)

                if status is False:
                    rospy.logerr("Error reading '" + field + "': " + reply)
                else:
                    if type(robot_buttons.__getattribute__(field)) is bool:
                        robot_buttons.__setattr__(field, bool(reply))
                    else:
                        robot_buttons.__setattr__(field, str(reply))

                time.sleep(serial_wait)
            rospy.loginfo(robot_buttons)
            pub_robot_buttons.publish(robot_buttons)

            #Read analog data
            robot_analog_values = RobotAnalogValues()
            fields = robot_analog_values.__slots__
            for field in fields:
                status, reply = comm.communication.instance.send_command("GET " + field)

                if status is False:
                    rospy.logerr( "Error reading '" + field + "': " + reply)
                else:
                    robot_analog_values.__setattr__(field, float(reply))

                time.sleep(serial_wait)
            rospy.loginfo(robot_analog_values)
            pub_robot_analog_values.publish(robot_analog_values)

            r.sleep()
        rospy.spin()

if __name__ == "__main__":
    try:
        ControlPanelServer()
    except rospy.ROSInterruptException:
        pass
