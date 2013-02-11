# true or false
simulation=False

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
use_websockets=True
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

Fan = 0
IMU = 1
Camera = 2
GPS = 3
Switch = 4
Lights = 5
RangeFinder = 6
Laptop = 7
Motors = 8

Tension = 9
Current = 10
Temperature = 11

EstopManual = 12
EstopRemote = 13

Mode = 14

