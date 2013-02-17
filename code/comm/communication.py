import string
import sys
import traceback

import config
from serial_com import SerialCom

class Debug:
    def write(self, values):
        for value in values:
            print hex(ord(value)) + ",",
        print "\n"


class NoDebug:
    def write(self, values):
        pass

# http://clubcapra.com/wiki/index.php/Contr%C3%B4leur_d%27alimentation
class Communication:
    """
    The communication class is responsible for responding to particular commands.
    A SerialComInstance can be pass to connect to a real serial or a mocked serial.
    """
    def __init__(self, SerialComInstance = SerialCom()):
        self.serial  = SerialComInstance


    def init(self):

        if config.debug is True:
            self.debug = Debug()
        self.serial.connect( \
                config.serial_port, \
                config.baudrate, \
                config.readTimeout)


    def shutdown(self):
        print "Closing serial connection."
        self.serial.close()


    def sendCommand(self, command):
        parts = string.split(command, " ")

        command = parts[0].upper()
        deviceId = self.get_sensor_addr(parts[1])
        if len(parts) > 2:
            state = parts[2]

        try:
            if command == "SET":
                self.serial.write(command + " " + str(deviceId) + " " + state.upper() + "\n")
                return True, None

            if command == "GET":
                self.serial.write(command + " " + str(deviceId) + " " + "\n")
                print "reading"
                statusInformation = self.serial.read(1024)
                print "read"
                return True, statusInformation
                
        except:
            traceback.print_exc(file=sys.stdout)
            return False, self.help()

        return False, self.help()

    def get_sensor_addr(self, name):
        for var, value in vars(config).items():
            if var.lower() == name.lower():
                return value
    
    def get_all_sensors(self):
        devices = []
        for name, value in vars(config).items():
            if name[0] is not "_" and len(str(value)) == 2:
                devices.append(name)
        return devices

    def help(self):
        helpMessage =  "Commands availables are:\n"
        helpMessage += "  SET   <sensorName> <value>\n" 
        helpMessage += "  GET  <sensorName>\n" 
        helpMessage += "where <value> is ON or OFF and <sensorName> is one of:\n"
        helpMessage += "  " + "\n  ".join(self.get_all_sensors())
        helpMessage += "\n"
        return helpMessage

    def checkSum(self, hexArray):
        # compute checksum from array
        checksum = 0x00
        for e in hexArray:
            if e == None:
                continue
            checksum += e

        # limit checksum
        while checksum > 0xFF:
            checksum -= 0xFF

        return checksum
