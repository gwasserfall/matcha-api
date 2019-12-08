from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required

from models.user import User

from helpers import Arguments

from pprint import pprint

class UserListResource(Resource):

    def post(self):

        args = Arguments(request.json)

        args.string("fname", required=True)
        args.string("lname", required=True)
        args.email("email", required=True)
        args.string("password", required=True)
        args.string("username", required=True)
        args.enum("gender", ["male", "female", "other"], required=True)
        args.string("bio", required=True)
        args.integer("age", required=True)
        args.decimal("longitude", required=True)
        args.decimal("latitude", required=True)

        new = User()

        from pprint import pprint

        pprint(new.test())

        args.validate()
        

        new = User().create(**args)
        if (new.insert()):
            
            return new.to_dict(), 200
        return {"message" : "Duplicate error"}, 400


class UserResource(Resource):
    
    @jwt_required
    def get(self, id):
        user = User.get(id=id)
        pprint(user.to_dict())
        return user.to_dict(), 200