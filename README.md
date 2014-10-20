capra_controlpanel
==================

ROS node to manage the hardware control panel of the robot. It can read data, like tension, current, temperature and button states, and activate or deactivate sensors. To add a sensor, its name must be added to the message (in /msg folder) and its name and ID(int defined on the board) must be added to the launchfile (in /launch). 

