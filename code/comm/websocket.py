
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import communication

class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print 'websocket: new connection'
      
    def on_message(self, data):
        print 'websocket: data received %s' % data
        
        status, reply = communication.instance.send_command(data)
        
        if reply is not None:
            print "websocket: sending response to client: " + reply
            self.write_message(reply)
 
    def on_close(self):
        print 'websocket connection closed'
 
class WebsocketServer:
    def __init__(self, port):
        print "websocket: opening on port " + str(port)
        application = tornado.web.Application([(r'/ws', WSHandler), ])
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
