from flask import Flask, render_template, request, session
from flask_restful import Resource, Api
from flask_socketio import SocketIO, join_room
from flask_jwt_extended import JWTManager


from helpers import jwt_refresh_required
from helpers import ModelEncoder

from resources import *

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")

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


clients = []

@socketio.on('connect')
def test_connect():
    print(request.sid + " has joined the fold")
    clients.append(request.sid)
    room = session.get('room')
    print(room)
    join_room(room)
    print(clients)
    socketio.emit('reply', {'message': 'has entered the room.'}, room=clients[-1])

@socketio.on('disconnect')
def test_disconnect():
    print("Disconnected")

# Need to move to seperate file
@socketio.on('message')
def handle_message(message):
    print(request.sid)
    socketio.emit("reply", {"message" : "We got " + message["message"]})
    print('received message: ' + message["message"])
    print(clients)

if __name__ == "__main__":
    socketio.run(app, debug=True)