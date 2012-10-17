#!/usr/bin/python

import SocketServer
import socket
import sys
import time
import traceback
from config import Config

from communication import Communication

class EchoClientHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print "client connected"
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            self.request.send(data)
        print "client disconnected"



# To enable a mock for the serial
import sys
sys.path.append("tests/")
from serial_com_mock import SerialComMock

# The communication interface to the sensors is defined globally
cfg = Config()
cfg.load("conf/simulation.conf")
if cfg.getValues()["simulation"].lower() == "true":
    comm = Communication(SerialComMock()) # a mocked serial implementation
else:
    comm = Communication() # real serial
comm.init()

class SensorsClientHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # TODO add a try catch and return stack trace to socket
        # http://docs.python.org/library/traceback.html
        try:
            self.inner_handle()
        except:
            traceback.print_exc(file=sys.stdout)
            message = "Invalid command"
            self.request.send(message)
            stacktrace = repr(traceback.format_stack())
            self.request.send(stacktrace)


    def inner_handle(self):
        print "client connected"
        data = None
        while not data:
            data = self.request.recv(1024)
            break

        print "data received: " + str(data)

        data = data.replace("\n", "")
        # TODO encure the comm is still connected or try reconnection on send command
        
        if data == "shutdown-server":
            self.server.shutdown()
            print "server stopped"
            
        
        isValidCommand, message = comm.sendCommand(data)
        if not message == None:
            print "sending response: "
            print message
            self.request.send(message)

        print "client disconnected"

class ReusableTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True


class ThreadedTCPServer(SocketServer.ThreadingMixIn, ReusableTCPServer):
	pass

def main(PORT):
    
    try:
        sock = socket.create_connection(("127.0.0.1", PORT))
        sock.send("shutdown-server")
        sock.close()
        print "Shutting down running server.."
        time.sleep(1)    
    except:
        pass
		#Executed when no other servers are running on this port

    server = ThreadedTCPServer( ("", PORT), SensorsClientHandler)
    print "starting server on port " + str(PORT) + "..."
    try:
        server.serve_forever()
        comm.shutdown();
    except KeyboardInterrupt:
        server.shutdown()
        comm.shutdown()
        print "server stopped"
        



if __name__ == "__main__":
    PORT = 53001
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    main(PORT)

