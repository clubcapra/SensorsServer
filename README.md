============= SensorsServer =============

Application used to transfer data from a socket to a serial port in the objective of communicating with the robot control panel.

=== Communication protocol ===

SET [id] [state]
GET [id]

[state] = ON or OFF
[id] = address of the device
    N_ for digital binary sensors like the GPS and the E-stop (N1, N2, etc.)
    A_ for analog data like the battery tension (A1, A2, etc.)
    The GET returns values accordingly (ON/OFF or an analog value)

