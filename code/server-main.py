#!/usr/bin/python

import SocketServer
import socket
import sys
import time
import traceback
import thread
import re

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import config

from comm.communication import Communication
from comm.serial_com_mock import SerialComMock

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

# The communication interface to the sensors is defined globally
if config.simulation is True:
    comm = Communication(SerialComMock()) # a mocked serial implementation
else:
    comm = Communication() # real serial
comm.init()

class SensorsClientHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        print "client connected"
        try:
            self.inner_handle()
        except:
            traceback.print_exc(file=sys.stdout)
            message = "Command error"
            self.request.send(message)
            stacktrace = repr(traceback.format_stack())
            self.request.send(stacktrace)

    def inner_handle(self):
        data = None
        while not data:
            data = self.request.recv(1024)

        print "socket: data received: " + str(data)
        
        data = data.replace("\n", "")
        
        if data == "shutdown-server":
            self.server.shutdown()
            print "socket server stopped"
            
        p1 = re.compile("[SETset]+ [0-9a-zA-Z]+ [ONFonf]+")
        p2 = re.compile("[GETget]+ [0-9a-zA-Z]+")
        
        if p1.match(data) is not None or p2.match(data) is not None:
            isValidCommand, message = comm.sendCommand(data)
            if not message == None:
                print "sending socket response: "
                print message
                self.request.send(message)
        else:
            print "Invalid command"
            self.request.send("Error: invalid message format\n")


class ReusableTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True


class ThreadedTCPServer(SocketServer.ThreadingMixIn, ReusableTCPServer):
    pass

def mainSocketServer(PORT):
    
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
    except KeyboardInterrupt:
        server.shutdown()
        raise
        
    comm.shutdown()
    print "server stopped"

class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print 'new connection on websocket'
        self.write_message("Capra 6: Bienvenue")
      
    def on_message(self, data):
        print 'websocket: message received %s' % data
        isValidCommand, message = comm.sendCommand(data)
        if not message == None:
                print "sending websocket response: "
                print message
                self.write_message(message)
 
    def on_close(self):
        print 'websocket connection closed'
 
class WebSocketService:
    def __init__(self, port):
        print "opening websocket on port " + str(port)
        application = tornado.web.Application([(r'/ws', WSHandler),])
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":

    if config.use_websockets is True:
        thread.start_new_thread(WebSocketService, (config.websocket_port,))
        
    if config.use_tcp_server is True:
        PORT = config.tcp_port
        if len(sys.argv) > 1:
            PORT = int(sys.argv[1])
         
        mainSocketServer(PORT)


