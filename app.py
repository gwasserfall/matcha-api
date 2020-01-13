from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from flask_socketio import SocketIO, join_room
from flask_jwt_extended import JWTManager

from helpers import jwt_refresh_required
from helpers import ModelEncoder

from resources import setup_socket_routes

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

# Dev
api.add_resource(ImageListResource, "/images")
api.add_resource(UserImagesResource, "/images/<str:username>")

# Requires token to infer viewer user id
api.add_resource(ProfileViewListResource, "/profile-view/<str:username>")

# Post when matches
api.add_resource(MatchListResource, "/matches")

# Can only see your own
api.add_resource(MatchResource, "/matches/<str:username>")
# Partial match and full match




setup_socket_routes(socketio)

@app.route("/")
def socket():
    return render_template("sockets.html")

@app.route("/clients")
def clients():
    print(chat.clients)
    return jsonify(chat.clients)

if __name__ == "__main__":
    debug = True if environment.lower() in ["dev", "development"] else False
    socketio.run(app, debug=debug, host="0.0.0.0" if debug else "127.0.0.1", port=5000)
