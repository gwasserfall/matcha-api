from flask import Flask
from flask_sockets import Sockets
from pprint import pprint

app = Flask(__name__)
app.debug = True
sockets = Sockets(app)

socks = []

@sockets.route('/register')
def register_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)

@sockets.route('/echo')
def echo_socket(ws):
    pprint(dir(ws))
    while not ws.closed:
        message = ws.receive()
        ws.send(message)

@sockets.route('/status')
def status_socket(ws):
    pprint(dir(ws))
    while not ws.closed:
        message = ws.receive()
        ws.send(message)


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()