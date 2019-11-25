from flask_restful import Resource, reqparse
from models.user import User

class UserList(Resource):
    def get(self):
        user = User()

        user.get(id="1")
        return {'hello'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fname', type=str, help='First name required', required=True)
        parser.add_argument('lname', type=str, help='Last name required', required=True)
        parser.add_argument('email', type=str, help='Email is required', required=True)
        parser.add_argument('password', type=str, help='Password is required', required=True)
        parser.add_argument('username', type=str, help='Username is required', required=True)
        parser.add_argument('gender', type=str, help='Gender is required', required=True)
        parser.add_argument('bio', type=str, help='Bio must be a string')
        parser.add_argument('age', type=int, help='Age is required', required=True)
        parser.add_argument('longitude', type=str)
        parser.add_argument('latitude', type=str)

        args = parser.parse_args()
        from pprint import pprint
        new = User().create(**args)
        if (new.insert()):
            pprint(new.to_dict())
            return new.to_dict(), 200
        return {"message" : "Duplicate error"}, 400