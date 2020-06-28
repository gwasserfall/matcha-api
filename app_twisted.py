
from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
import signal


from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource, WSGIRootResource


from flask import Flask, render_template, request, jsonify, g
from flask_restful import Resource, Api

from flask_socketio import SocketIO, join_room
from flask_jwt_extended import JWTManager


from flask_cors import CORS

from helpers import jwt_refresh_required
from helpers import ModelEncoder


from config import environment

import sys


from models import connection

from resources import *

app = Flask(__name__)

with app.app_context():
    g.hello = "hi"


app.debug = True

CORS(app)

#socketio = SocketIO(app, cors_allowed_origins="*")
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SECRET_KEY'] = 'super-secret'
app.config['RESTFUL_JSON'] = {
    "cls": ModelEncoder,
    "encoding" : "utf-8"}

jwt = JWTManager(app)

api = Api(app, prefix="/v1")
#api = Api(app, prefix="/v1")


# TODO: Document for pair programming
api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/user/<int:id>")
api.add_resource(LoginResource, "/login")

api.add_resource(ValidationResource, '/validate/<string:code>')
api.add_resource(ValidationRetryResource, '/validate/resubmit/<string:email>')


api.add_resource(VerifyTokenResource, "/verify-token")



# Our WebSocket Server protocol
class EchoServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        log.msg(self.http_headers)
        #self.sendMessage(payload, isBinary)
    
    def onConnect(self, request):
        log.msg("Client connecting: {}".format(request.peer))

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)



class BroadcastServerFactory(WebSocketServerFactory):
  
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []


    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        print(self.clients)
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            print("message sent to {}".format(c.peer))



# Dev
# api.add_resource(ImageListResource, "/images")
# api.add_resource(UserImagesResource, "/images/<str:username>")

# Requires token to infer viewer user id
# api.add_resource(ProfileViewListResource, "/profile-view/<str:username>")

# Post when matches
# api.add_resource(MatchListResource, "/matches")

# Can only see your own
# api.add_resource(MatchResource, "/matches/<str:username>")
# Partial match and full match


if __name__ == "__main__":
    debug = True if environment.lower() in ["dev", "development"] else False
    
    log.startLogging(sys.stdout)

    # create a Twisted Web resource for our WebSocket server
    wsFactory = BroadcastServerFactory("ws://0.0.0.0:5000")
    #wsFactory.protocol = EchoServerProtocol


    app.socks = wsFactory

    wsResource = WebSocketResource(wsFactory)

    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)

    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    site = Site(rootResource)

    signal.signal(signal.SIGINT, signal.default_int_handler)
    reactor.listenTCP(5000, site)
    reactor.run()









