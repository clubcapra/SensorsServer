import string
import sys
import traceback

from sensors_mapping import SensorsMapping
from serial_com import SerialCom
from serial_config import SerialConfig


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
        self.mapping = SensorsMapping()
        self.serial  = SerialComInstance

        self.messagesParts = \
                { \
                  "start" : { \
                    "function" : 0x00, \
                    "size"     : 0x03}, \
                  "stop" : { \
                    "function" : 0x01,  \
                    "size"     : 0x03}, \
                  "status" : { \
                    "function" : 0x02,
                    "size"     : 0x02}, \
                  "battery-state" : { \
                    "function" : 0x03,
                    "size"     : 0x02} \
                }


    def init(self):
        # load mapping for sensors
        self.mapping.load("conf/sensors-mapping.conf")

        # load serial driver
        serialConfig = SerialConfig()

        serialConfig.load("conf/serial.conf")
        if serialConfig.getValues()["debug"].lower() == "true":
            self.debug = Debug()
        self.serial.connect( \
                serialConfig.getValues()["port"], \
                serialConfig.getValues()["baudrate"], \
                serialConfig.getValues()["readTimeout"])


    def shutdown(self):
        print "Closing serial connection."
        self.serial.close()


    def sendCommand(self, command):
        parts = string.split(command, " ")

        first = parts[0]
        second = None
        if len(parts) > 1:
            second = parts[1]

        try:
            if first == "stop":
                self.stop(second)
                return True, None

            if first == "start":
                self.start(second)
                return True, None

            if first == "status":
                statusInformation = self.status(second)
                return True, statusInformation

            if first == "battery-state":
                batteryStateInformation = self.batteryState()
                return True, batteryStateInformation
                
        except:
            traceback.print_exc(file=sys.stdout)
            return False, self.help()

        return False, self.help()


    def stop(self, arg):
        self.parseArgsThenSend(self.messagesParts["stop"], arg)


    def start(self, arg):
        self.parseArgsThenSend(self.messagesParts["start"], arg)


    def status(self, arg):
        self.parseArgsThenSend(self.messagesParts["status"], arg)
        stateResponse = self.serial.read(5)

        #print "state response: " + stateResponse
        statusHex = stateResponse[3]
        statusBin = bin(ord(statusHex))[2:]

        if len(statusBin) < 8:
            nbMissing = 8 - len(statusBin)
            statusBin = ('0' * nbMissing) + statusBin

        if self.debug:
            print "state response: "
            self.debug.write(stateResponse);
            print statusBin

        return self.toHumanReadableStatus(statusBin)


    def batteryState(self):
        self.parseArgsThenSend(self.messagesParts["battery-state"], None)
        batteryStateResponse = self.serial.read(8)
        voltageLow  = ord(batteryStateResponse[3])
        voltageHigh = ord(batteryStateResponse[4])
        ampereLow   = ord(batteryStateResponse[5])
        ampereHigh  = ord(batteryStateResponse[6])

        return self.toHumanReadableBatteryState(voltageLow, voltageHigh, ampereLow, ampereHigh)

    
    def toHumanReadableStatus(self, statusBin):
        information = []

        for key in self.mapping.getValues().keys():
            val = self.mapping.getValues()[key]
            line = key + " = " + str(statusBin[7 - val])
            information.append(line)
        information.append("\n")
        
        return "\n".join(information)


    def toHumanReadableBatteryState(self, voltageLow, voltageHigh, ampereLow, ampereHigh):
        information = []
        voltage = self.getVoltageFromRawHex(self.to16BitsValue(voltageLow, voltageHigh))
        ampere = 0. #self.to16BitsValue(ampereLow, ampereHigh)

        information.append("voltage: " + str(voltage) + "V")
        information.append("current: "  + str(ampere) + "A")
        information.append("\n")

        return "\n".join(information)


    def to16BitsValue(self, low, high):
        return ((high & 0xF) << 8) + int(low)

	def getVoltageFromRawHex(self, rawHex):
		ADC_MAX = (2. ** 12) - 1.
		MAX_VOLTAGE = 60.
		BOARD_SUPPLY = 4.97
		MAX_SIGNAL_INPUT = 5.
		return rawHex * BOARD_SUPPLY / ADC_MAX * MAX_VOLTAGE / MAX_SIG_INPUT
		

    def help(self):
        helpMessage =  "Commands availables are:\n"
        helpMessage += "  stop   <sensorName>\n" 
        helpMessage += "  start  <sensorName>\n" 
        helpMessage += "  status [<sensorName>]\n" 
        helpMessage += "  battery-state\n" 
        helpMessage += "where <sensorName> is one of:\n"
        helpMessage += "  " + "\n  ".join(self.mapping.getValues().keys())
        helpMessage += "\n"
        return helpMessage


    def parseArgsThenSend(self, messagesParts, sensorId):
        value = None
        if sensorId == None:
            value = None
        else:
            key = string.strip(sensorId, " \t")
            value = (1 << self.mapping.getValues()[key])
        self.sendBytes(messagesParts["function"], messagesParts["size"], value)


    def sendBytes(self, function, size, value):
        values = [size, function, value]
        values.append(self.checkSum(values))
        formatedMessage = self.formatMessage(values)
        if self.debug:
            print "sending message: "
            self.debug.write(formatedMessage)
        self.serial.write(formatedMessage)


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


    def formatMessage(self, hexArray):
        START = chr(0xAA)
        message = START
        for t in hexArray:
            if t == None: 
                continue
            message = message + chr(t)

        return message

