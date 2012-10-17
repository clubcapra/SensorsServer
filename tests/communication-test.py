#!/bin/usr/python

import unittest

# add src folder in path to resolve imports
import sys
sys.path.append("src/")

from communication import Communication
from serial_com_mock import SerialComMock


class CommunicationTest(unittest.TestCase):

    def testCheckSum(self):
        comm = Communication()
        checksum = comm.checkSum([0x01, 0x02, 0x03])

        self.assertEqual(0x06, checksum)


    def testCheckSumOverflow(self):
        comm = Communication()
        checksum = comm.checkSum([0x55, 0xAB])

        self.assertEqual(0x01, checksum)


    def createSerialAndCommunication(self):
        serial = SerialComMock()
        comm = Communication(serial)
        comm.init()

        return serial, comm


    def testSendCommand(self):
        serial, comm = self.createSerialAndCommunication()

        comm.sendCommand("stop RangeFinder")

        self.assertEqual(self.formatMessage([0xAA, 0x03, 0x01, 0x02, 0x06]), serial.written[0])

    
    def testSendStatus(self):
        serial, comm = self.createSerialAndCommunication()

        result = comm.sendCommand("status")


    def testTo16BitsValue(self):
        serail, comm = self.createSerialAndCommunication()

        result = comm.to16BitsValue(60., 0xFF, 0x07)

        self.assertEqual(30., round(result))


    def testSendBatteryState(self):
        serial, comm = self.createSerialAndCommunication()

        result = comm.sendCommand("battery-state")

        self.assertEquals(self.formatMessage([0xAA, 0x02, 0x03, 0x05]), serial.written[0])

    
    def testHelp(self):
        serial, comm = self.createSerialAndCommunication()

        helpMessage = comm.help()

        self.assertTrue(helpMessage != None)

    
    def formatMessage(self, hexArray):
        message = ""
        for e in hexArray:
            message += chr(e)
        return message

if __name__ == "__main__":
    unittest.main()



