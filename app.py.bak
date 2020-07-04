from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from flask_socketio import SocketIO, join_room
from flask_jwt_extended import JWTManager
from flask_restful_swagger import swagger
from flask_cors import CORS

from helpers import jwt_refresh_required
from helpers import ModelEncoder

from resources import setup_socket_routes

from config import environment


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
    "encoding" : "utf-8"
    }

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

# Dev
# api.add_resource(ImageListResource, "/images")
# api.add_resource(UserImagesResource, "/images/<str:username>")

# Requires token to infer viewer user id
# api.add_resource(ProfileViewListResource, "/profile-view/<str:username>")

# Post when matches
# api.add_resource(MatchListResource, "/matches")

# Can only see your own
# api.add_resource(MatchResource, "/matches/<str:username>")
# Partial match and full match




setup_socket_routes(socketio)

@app.route("/")
def socket():
    return render_template("sockets.html")


# Close database connection on exit
def close_connection():
	print("Closing Database Connection")
	connection.close()

import atexit

if __name__ == "__main__":
    debug = True if environment.lower() in ["dev", "development"] else False
    atexit.register(close_connection)
    socketio.run(app, debug=debug, host="0.0.0.0", port=5000)
