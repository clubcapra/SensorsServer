
class SerialComMock:

    def __init__(self):
        self.written = []
        self.connected = False


    def load(self, configFile):
        pass
    

    def connect(self, port, baudrate, readTimeout):
        self.connected = True


    def read(self, size):
        return "mock-lecture"


    def write(self, data):
        print "writing(sim): " + data
        self.written.append(data)

