
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

from sockets import get_server_factory, get_server_protocol
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

import ast
from markdown import markdown
import os

@app.route("/socks")
def socks():
  return render_template("sockets.html")

@app.route("/")
def documentation():
  
  docs = []

  for py in [os.path.join("resources", x) for x in os.listdir("resources") if "__" not in x and x.endswith("py")]:
    with open(py) as f:
        code = ast.parse(f.read())

    for node in ast.walk(code):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node)
            if docstring:
                
                endpoint = docstring.split("\n")[0]
                md = "\n".join(docstring.split("\n")[1:])
                print(md)
                docs.append(
                  {
                    "endpoint" : endpoint,
                    "docstring" : markdown(md, extensions=['fenced_code', 'attr_list'])
                  }
                )
  return render_template("api-docs.html", docs=docs)

import json
from models import user

class MatchaServerProtocol(WebSocketServerProtocol):
  
  # def onOpen(self):
  #     self.factory.register(self)

  def onMessage(self, payload, isBinary):
    with app.app_context():
        if not isBinary:
            try:
                valid_request = self.factory.authenticated(json.loads(payload), self)
                if valid_request:
                  self.routeMessage(valid_request)
                else:
                  print("Request is not authenticated, dropping..")
            except Exception as e:
                print("asdasdasd")
                print(str(e))

  def routeMessage(self, req):
    """
    Only authenticated messages get routed
    """
    method = req.get("method", None)

    print(f"{method} called")

    if method == "register":
      print("")
    elif method == "message":
      self.factory.sendMessage(req)
    elif method == "pollOnline":
      self.factory.pollOnline(self)
    else:
      print(f"Unknown method : {method}")
    

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

  def pollOnline(self, socket):
    print("Poll Online")
    payload = {
      "method" : "pollOnline",
      "content" : [{"id" : x["id"], "username" : x["username"]} for x in self.online]
    }
    socket.sendMessage(json.dumps(payload).encode("utf8"))

  def authenticated(self, req, socket):
    with app.app_context():
        try:
            user = decode_token(req["jwt"])
            username = user["identity"]["username"]
            user_id = user["identity"]["id"]
            on = list(filter(lambda x: x["username"] == username, self.online))

            if len(on) == 1:
                if socket not in on[0]["sockets"]:
                  on[0]["sockets"].append(socket) 
            else:
                self.online.append({"username": username, "sockets": [socket], "id" : user_id})
            
            req["sender"] = user["identity"]
            del req["jwt"]
            return req

        except Exception as e:
            print("Exception thrown in authenticate", str(e))
            print("Could not authenticate")
            return None

  def sendMessage(self, req):
    """
    Add message to database and send over socket if user is online
    """
    print("Message Request", req)
    to = req["content"].get("to", None)
    for client in self.online:
      if client["username"] == to or client["id"] == to:
        # Client is online
        payload = {
          "method" : "message",
          "content" : {
            "from" : req["sender"]["username"],
            "message" : req["content"]["message"]
          }
        }
        for socket in client["sockets"]:
          print("Sending message to online user", client["username"])
          socket.sendMessage(json.dumps(payload).encode("utf8"))







if __name__ == "__main__":
    debug = True if environment.lower() in ["dev", "development"] else False
    
    log.startLogging(sys.stdout)

    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)

    MatchaServerFactoryA = get_server_factory(app)
    MatchaServerProtocolA = get_server_protocol(app)

    wsFactory = MatchaServerFactoryA("ws://0.0.0.0:5000")
    wsFactory.protocol = MatchaServerProtocolA


    app.socks = wsFactory

    wsResource = WebSocketResource(wsFactory)


    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    site = Site(rootResource)

    signal.signal(signal.SIGINT, signal.default_int_handler)
    reactor.listenTCP(5000, site)
    reactor.run()









