
class SerialComMock:

    def __init__(self):
        self.written = []
        self.connected = False


    def load(self, configFile):
        pass
    

    def connect(self, port, baudrate, readTimeout):
        self.connected = True


    def read(self, size):
        SENSORS_STATE_LEN = 5
        BATTERY_STATE_LEN = 8
        if size == SENSORS_STATE_LEN:
            return [0xAA, 0x03, 0x02, 0x0F, 0x14]
        if size == BATTERY_STATE_LEN:
            return [0xAA, 0x06, 0x03, 0x0F, 0x7F, 0x95, 0x04, 0x30]

        raise Exception("The communication mock does not support read message size of: " + str(size))


    def write(self, data):
        self.written.append(data)

