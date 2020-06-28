from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol

# Our WebSocket Server protocol
class EchoServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        log.msg(self.http_headers)
        self.sendMessage(payload, isBinary)
    
    def onConnect(self, request):
        log.msg("Client connecting: {}".format(request.peer))

        log.msg(dir(request))



class BroadcastServerFactory(WebSocketServerFactory):
  
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.tickcount = 0
        self.tick()

    def tick(self):
        self.tickcount += 1
        self.broadcast("tick %d from server" % self.tickcount)
        reactor.callLater(1, self.tick)

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

