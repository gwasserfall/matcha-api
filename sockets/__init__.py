import json
from models import user
from pprint import pprint
from twisted.internet import reactor
from flask_jwt_extended import decode_token

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol

def get_server_protocol(app):

    class MatchaServerProtocol(WebSocketServerProtocol):

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
                self.factory.sendPollOnlineRequest()
            elif method == "message":
                self.factory.sendMessage(req)
            elif method == "pollOnline":
                self.factory.pollOnline(self)
            else:
                print(f"Unknown method : {method}")


        def connectionLost(self, reason):
            WebSocketServerProtocol.connectionLost(self, reason)
            self.factory.unregister(self)

    return MatchaServerProtocol


def get_server_factory(app):

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
                    self.sendPollOnlineRequest()

        def pollOnline(self, socket):
            print("Poll Online")
            payload = {
              "method" : "pollOnline",
              "content" : [{"id" : x["id"], "username" : x["username"]} for x in self.online]
            }
            socket.sendMessage(json.dumps(payload).encode("utf8"))

        def sendPollOnlineRequest(self):
            payload = {
              "method" : "pollOnlineRequest",
              "content" : None
            }
            for user in self.online:
                for socket in user["sockets"]:
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

    return MatchaServerFactory
