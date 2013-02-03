# true or false
simulation=True

# The default baudrate is 19200. 
# It should not change since its defined this way on the hardware.

serial_port="/dev/ttyUSB0"
baudrate=19200
readTimeout=1000
debug=True

# TCP server
use_tcp_server=True
tcp_port=53001

# Websocket
use_websockets=False
websocket_port=53002

# This section is intended to represent a mapping of the different 
# sensors and their association with their alimentation id
#
# ex:
#
# RangeFinder = 1
#
# No spaces allowed in names
# Lines starting with # are comments
# Ids goes from 0 to 7
#

Camera = "N0"
RangeFinder = "N1"
GPS = "N2"
IMU = "N3"
Lights = "N4"
Motors = "N5"
S6 = "N6"
S7 = "N7"

Tension = "A0"
Current = "A1"
Temperature = "A2"
