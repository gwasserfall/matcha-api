import json
from models.user import User
from models.matches import Match
from models.message import Message
from twisted.internet import reactor
from flask_jwt_extended import decode_token


from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.exception import Disconnected


def get_server_protocol(app):

    class MatchaServerProtocol(WebSocketServerProtocol):

        def onMessage(self, payload, isBinary):

            with app.app_context():
                if not isBinary:
                    try:
                        valid_request = self.factory.authenticated(json.loads(payload), self)
                        if valid_request:
                            self.routeMessage(valid_request)
                    except Exception as e:
                        pass

        def routeMessage(self, req):
            """
            Only authenticated messages get routed
            """
            method = req.get("method", None)

            if method == "register":
                pass
            elif method == "message":
                self.factory.routeUserMessage(req)
            elif method == "pollOnline":
                self.factory.pollOnline(self)
            elif method == "initChat":
                self.factory.initiateChat(self, req)
            elif method == "getMessagesFor":
                self.factory.sendMessagesFrom(self, req)
           


        def connectionLost(self, reason):
            WebSocketServerProtocol.connectionLost(self, reason)
            self.factory.unregister(self)
            

        def __repr__(self):
            username = getattr(self, "user")
            if username:
                return "<Socket : [{}]>".format(username)
            else:
                return super.__repr__()

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
            # self.list_clients()

        # def list_clients(self):
        #     print("Clients")
        #     pprint(self.online)
        #     reactor.callLater(5, self.list_clients)

        def initiateChat(self, socket, payload):
            to = payload["content"]["username"]
            #print(socket.user, "wants to chat to", payload["content"]["username"])

        def unregister(self, socket):
            for user in self.online:
                if socket in user["sockets"]:
                    user["sockets"].remove(socket)
                if len(user["sockets"]) == 0:
                    self.online.remove(user)
                    self.sendPollOnlineRequest()
            
        def pollOnline(self, socket):
            
            ## TODO check for matches
            payload = {
              "method" : "pollOnlineResponse",
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
                    try:
                        socket.sendMessage(json.dumps(payload).encode("utf8"))
                    except Disconnected:
                        pass

        def sendMessagesFrom(self, socket, req):
            from_user = User.get(username=req["content"]["username"])

            messages = from_user.get_messages(req["sender"]["id"])

            payload = {
                "method" : "receiveMessagesFrom",
                "content" : {
                    "messages" : messages
                }
            }
            socket.sendMessage(json.dumps(payload, default=str).encode("utf8"))
            pass

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
                        self.sendPollOnlineRequest()

                    socket.user = username
                    socket.user_id = user_id

                    req["sender"] = user["identity"]
                    del req["jwt"]
                    return req

                except Exception as e:
                    return None

        def routeUserMessage(self, req):
            """
            Add message to database and send over socket if user is online
            """
            
            to = req["content"].get("to", None)
            
            to_user = User.get(username=to)
            from_user_id = req["sender"]["id"]

            online = False

            message = Message(to_id=to_user.id, from_id=from_user_id, message=req["content"]["message"])

            for client in self.online:
                if client["username"] == to or client["id"] == to:
                    online = True
                    payload = {"method" : "refreshMessages"}
                    for socket in client["sockets"]:
                        socket.sendMessage(json.dumps(payload).encode("utf8"))

            message.seen = online
            message.save()


    return MatchaServerFactory
