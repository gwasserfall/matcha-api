from flask import Flask
from flask_restful import Resource, Api

from resources.users import UserList

app = Flask(__name__)
api = Api(app)

# db = records.Database('sqlite:///database.sqlite3')

api.add_resource(UserList, '/users')

if __name__ == '__main__':
    app.run(debug=True)