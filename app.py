from flask import Flask
from flask_restful import Resource, Api
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager

from helpers import jwt_refresh_required
from helpers import ModelEncoder

from config import environment

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


# Need to move to seperate file
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass


if environment.lower() in ["dev", "development"]:
    debug = True
else:
    debug = False

if __name__ == "__main__":
    socketio.run(app, debug=debug, host="0.0.0.0" if debug else "127.0.0.1", port=5000)
