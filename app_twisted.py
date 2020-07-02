
from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
import signal


from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource, WSGIRootResource


from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api

from flask_socketio import SocketIO, join_room
from flask_jwt_extended import JWTManager, decode_token


from flask_cors import CORS

from helpers import jwt_refresh_required
from helpers import ModelEncoder

from pprint import pprint

from config import environment

import sys

from models import connection

from resources import *

app = Flask(__name__)


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

api.add_resource(MatchListResource, "/matches")
api.add_resource(MatchResource, "/match/<int:user_id>")

api.add_resource(RatingResource, "/rating/<int:user_id>")

api.add_resource(PasswordResetRequestResource, "/reset-password-request")
api.add_resource(PasswordChangeResource, "/reset-password")








    # def broadcast(self, msg):
    #     print("broadcasting message '{}' ..".format(msg))
    #     print(self.clients)
    #     for c in self.clients:
    #         c.sendMessage(msg.encode('utf8'))
    #         print("message sent to {}".format(c.peer))


import json
from models import user

class MatchaServerProtocol(WebSocketServerProtocol):
  
  # def onOpen(self):
  #     self.factory.register(self)

  def onMessage(self, payload, isBinary):
    with app.app_context():
        if not isBinary:
            try:
                req = json.loads(payload)

                # Route message depending on method
                self.routeMessage(req)
            except Exception as e:
                print("asdasdasd")
                print(str(e))

  def routeMessage(self, req):
    method = req.get("method", None)

    user = decode_token(req["token"])

    if method == "authenticate":
      self.factory.authenticate(req, self)
    if method == "sendMessage":
      self.factory.sendMessage(req)
    if method == "pollOnline":
      self.factory.pollOnline(req)
    

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)


class MatchaServerFactory(WebSocketServerFactory):

  """
  Simple broadcast server broadcasting any message it receives to all
  currently connected clients.
  """

  def __init__(self, url):
    WebSocketServerFactory.__init__(self, url)
    self.online = []
    # self.clients = []
    self.list_clients()

  def list_clients(self):
    print("Clients")
    pprint(self.online)
    reactor.callLater(20, self.list_clients)

  def unregister(self, socket):
    for user in self.online:
      if socket in user["sockets"]:
        user["sockets"].remove(socket)
      if len(user["sockets"]) == 0:
        self.online.remove(user)


  def get_online_user(self, username):
    pass


  def authenticate(self, req, socket):
    with app.app_context():
        try:
            user = decode_token(req["token"])
            username = user["identity"]["username"]
            user_id = user["identity"]["id"]
            on = list(filter(lambda x: x["username"] == username, self.online))

            if len(on) == 1:
                on[0]["sockets"].append(socket)
            else:
                self.online.append({"username": username, "sockets": [socket], "id" : user_id})

        except Exception as e:
            print(str(e))
            print("Could not authenticate")

  def sendMessage(self, req):
    for client in self.online:
      for socket in client["sockets"]:
        print("Sending message to ", client["username"])
        socket.sendMessage(json.dumps({"method": "message"}).encode("utf8"))







if __name__ == "__main__":
    debug = True if environment.lower() in ["dev", "development"] else False
    
    log.startLogging(sys.stdout)

    # create a Twisted Web resource for our WebSocket server
    # with app.app_context():
    #     wsFactory = MatchaServerFactory("ws://0.0.0.0:5000")
    #     wsFactory.protocol = MatchaServerProtocol

    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)
    wsFactory = MatchaServerFactory("ws://0.0.0.0:5000")
    wsFactory.protocol = MatchaServerProtocol


    app.socks = wsFactory

    wsResource = WebSocketResource(wsFactory)


    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    site = Site(rootResource)

    signal.signal(signal.SIGINT, signal.default_int_handler)
    reactor.listenTCP(5000, site)
    reactor.run()









