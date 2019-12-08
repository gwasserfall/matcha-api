from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from resources import UserListResource
from resources import UserResource
from resources import LoginResource

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

api = Api(app, prefix="/v1")

api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/user/<int:id>")
api.add_resource(LoginResource, "/login")

if __name__ == "__main__":
    app.run(debug=True)