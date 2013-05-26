import traceback
import SocketServer
import sys
import socket
import time
import communication

class TcpServer:
    
    def __init__(self, port):
        self.port = port
        
    def start(self):
        try:    
            sock = socket.create_connection(("127.0.0.1", self.port))
            sock.send("shutdown-server")
            sock.close()
            print "tcpsocket: Shutting down running server.."
            time.sleep(1)    
        except:
            pass
            #Executed when no other servers are running on this port
    
        server = ThreadedTCPServer( ("", self.port), SensorsClientHandler)
        print "tcpsocket: starting server on port " + str(self.port) + "..."
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
            raise
            
        print "tcpsocket: server stopped"

class ReusableTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True


class ThreadedTCPServer(SocketServer.ThreadingMixIn, ReusableTCPServer):
    pass

class SensorsClientHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        print "tcpsocket: client connected"
        try:
            self.inner_handle()
        except:
            traceback.print_exc(file=sys.stdout)
            message = "tcpsocket: Command error"
            self.request.send(message)
            stacktrace = repr(traceback.format_stack())
            self.request.send(stacktrace)

    def inner_handle(self):
        data = None
        while not data:
            data = self.request.recv(1024)

        print "tcp socket: data received:' " + str(data) + "'"
        
        data = data.replace("\n", "")
        
        if data == "shutdown-server":
            self.server.shutdown()
            print "tcpsocket: socket server stopped"
        
        status, reply = communication.instance.send_command(data)
        
        if reply is not None:
            print "tcpsocket: sending response to client: " + reply
            self.request.send(reply)
        