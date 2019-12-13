from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from flask_socketio import SocketIO, join_room
from flask_jwt_extended import JWTManager


from helpers import jwt_refresh_required
from helpers import ModelEncoder

from config import environment

from chat import ChatController

from resources import *

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")
chat = ChatController(socketio)

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SECRET_KEY'] = 'super-secret'
app.config['RESTFUL_JSON'] = {
    "cls": ModelEncoder,
    "encoding" : "utf-8"
    }

jwt = JWTManager(app)

api = Api(app, prefix="/v1")

api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/user/<int:id>")
api.add_resource(LoginResource, "/login")


@app.route("/")
def socket():
    return render_template("sockets.html")

@app.route("/clients")
def clients():
    print(chat.clients)
    return jsonify(chat.clients)


@socketio.on('connect')
def socket_register():
    return chat.register(request.sid)

@socketio.on('disconnect')
def socket_disconnect():
    chat.disconnect(request.sid)

@socketio.on('send-message')
def socket_relay_message(data):
    chat.relay_message(data)

@socketio.on_error()
def error_handler(e):
    print(str(e))


if __name__ == "__main__":
    debug = True if environment.lower() in ["dev", "development"] else False
    socketio.run(app, debug=debug, host="0.0.0.0" if debug else "127.0.0.1", port=5000)
