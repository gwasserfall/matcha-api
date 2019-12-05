from flask import Flask
from flask_restful import Resource, Api

from resources import UserList

app = Flask(__name__)

api = Api(app, prefix='/v1')

api.add_resource(UserList, '/users')

if __name__ == '__main__':
    app.run(debug=True)