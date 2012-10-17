#!/usr/bin/python

# http://clubcapra.com/wiki/index.php/Contr%C3%B4leur_d%27alimentation

import serial
import time


def debug():
    pass


class SerialCom:

    def __init__(self):
        pass

    def connect(self, port, baudrate, readTimeout):
        self.port = serial.Serial(
                port, \
                baudrate, \
                serial.EIGHTBITS, \
                serial.PARITY_NONE, \
                serial.STOPBITS_ONE, \
                readTimeout)
        
    def write(self, data):
        #debug "writing:" + data
        print self.port.isOpen();
        self.port.write(data)

    def read(self, size):
        return self.port.read(size)

    def close(self):
        self.port.close()
    

def formatMessage(tableau):
    string = "" 
    for t in tableau:
        string = string + chr(t)
    return string
    

def tests():
    com = SerialCom()
    com.connect("/dev/ttyUSB0", 19200, 1000)
    while True:
        time.sleep(1.5)
        trame = [0xFF, 0x02, 0x02, 0x04]
        #trame = [0xFF, 0x03, 0x01, 0xFF, 0x03]
        #trame = [0xFF, 0x03, 0x01, 0x01, 0x05]
        com.write(formatMessage(trame))
        time.sleep(1.5)
        #trame = [0xFF, 0x03, 0x00, 0xFF, 0x02]
        #trame = [0xFF, 0x03, 0x00, 0x01, 0x04]
        #com.write(formatMessage(trame))
        print "Reading"
        print com.read(5)
        print "Done reading"
    
    com.close()
    #time.sleep(1)
    #com.write(formatMessage(trame))

if __name__ == "__main__":
    tests()

