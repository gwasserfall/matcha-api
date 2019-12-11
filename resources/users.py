from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import get_jwt_identity
from helpers import jwt_refresh_required

from models.user import User

from helpers import Arguments

from pprint import pprint



class UserListResource(Resource):

    def get(self):

        args = Arguments(request.json)
        args.date("dob", required=True)
        args.validate()

        return {"asd" : "asd"}, 200


    def post(self):

        args = Arguments(request.json)
        args.string("fname", required=True)
        args.string("lname", required=True)
        args.email("email", required=True)
        args.string("password", required=True)
        args.string("username", required=True)
        args.enum("gender", ["male", "female", "other"], required=True)
        args.string("bio", required=True)
        args.date("dob", required=True)
        args.decimal("longitude", required=True)
        args.decimal("latitude", required=True)
        args.validate()

        if User.get(username=args.username):
            return {"message" : "Username already exists"}, 400

        if User.get(email=args.email):
            return {"message" : "Email address already exists"}, 400

        new = User(dict(args))

        if (new.save()):
            return dict(new), 200
        else:
            return {"message" : "Falied to create user"}, 500



class UserResource(Resource):
    @jwt_refresh_required
    def get(self, id):
        
        current_user = get_jwt_identity()
        user = User.get(id=id)

        user.gender = "females"

        user.save()


        if not user:
            return {"message" : "User does not exist"}, 404

        if user.id != current_user["id"]:
            return user.essential(), 200
        else:
            return user, 200
