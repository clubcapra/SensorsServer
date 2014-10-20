
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
      #  print 'websocket: new connection'
        print "allo vincent"
      
    def on_message(self, data):
        if data == "w":
            print "EN AVANT"
        elif data == "a":
            print "gauche"
        elif data == "d":
            print "droite"
        pass
 
    def on_close(self):
        print 'websocket connection closed'
 
class WebsocketServer:
    def __init__(self):
        pass
    
    def start(self, port):
        print "websocket: opening on port " + str(port)
        application = tornado.web.Application([(r'/ws', WSHandler), ])
        self.http_server = tornado.httpserver.HTTPServer(application)
        self.http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
