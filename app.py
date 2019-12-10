from flask import Flask
from flask_restful import Resource, Api
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager

from helpers import jwt_refresh_required
from helpers import MatchaJSONEncoder

from resources import UserListResource
from resources import UserResource
from resources import LoginResource

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SECRET_KEY'] = 'super-secret'
app.config['FLASK_JSON'] = {'separators': (', ', ': '),
                            'indent': 2,
                            'cls': MatchaJSONEncoder}
jwt = JWTManager(app)

api = Api(app, prefix="/v1")

api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/user/<int:id>")
api.add_resource(LoginResource, "/login")


# Need to move to seperate file
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

if __name__ == "__main__":
    socketio.run(app, debug=True)