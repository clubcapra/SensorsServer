= Description

This projet is a server to allow a remote client to control the state of the sensors.
More information about the hardware can be found here:
http://clubcapra.com/wiki/index.php/Contr%C3%B4leur_d%27alimentation


A client can connect through a TCP connection and send commands

The application can be configured through the src/config/ classes

= Prerequisits
Look at the conf folder. From there you can enable or disable the simulation of the board. 
You can also define ids associated to sensors by their names.
Its also possible to change the baudrate and port used for the serial.

python-pip - easy_install to install python dependencies

= Serial communication protocol

SET [id] [state]\n
GET [id]\n

[state] = ON or OFF
[id] = address of the device
    N_ for digital binary sensors like the GPS and the E-stop (N0, N1, etc.)
    A_ for analog data like the battery tension (A0, A1, etc.)
    The GET returns values accordingly (ON/OFF or an analog value)

= References

How to create a connection in python:
http://docs.python.org/library/socket.html#example

How to create a thread in python:
http://www.shocksolution.com/2008/08/python-threads-are-easy-with-example/

How to use a synchronized queue in python:
http://docs.python.org/library/queue.html#queue-objects
