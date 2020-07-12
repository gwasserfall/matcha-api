from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import get_jwt_identity
from helpers import jwt_refresh_required

from helpers.genders import genders
from helpers.email import send_validation_email

from models.user import User, get_full_user
from models.validation import Validation

import secrets

from helpers import Arguments

import traceback

class UserListResource(Resource):

    def get(self):

        # Filtering should be here in something

        args = Arguments(request.json)
        args.date("dob", required=True)
        args.validate()

        return {"asd" : "asd"}, 200


    def post(self):
        """
        Posting to userlist = Registration
        """

        args = Arguments(request.json)
        args.email("email", required=True)
        args.string("username", required=True, min=3, max=255)
        args.string("password", required=True, max=255)
        args.string("fname", required=True, min=1, max=255)
        args.string("lname", required=True, min=1, max=255)
        #args.string("gender", required=True, enum=genders)

        # Validate method will abort with 400 if needed
        args.validate()

        if User.get(username=args.username):
            return {"message" : "Username already exists"}, 400

        if User.get(email=args.email):
            return {"message" : "Email address already exists"}, 400

        try:
            new = User(dict(args))
            new.save()
        except Exception as e:
            return {"message" : str(e)}, 500

        user = User.get(username=args.username)

        # Create validation entry and send email with verify link
        try:
            validation = Validation(user_id=user.id, code=secrets.token_urlsafe(256))
            validation.save()
        except Exception as e:
            return {"message" : str(e)}, 500

        send_validation_email(user, validation.code)

        return user, 200


class UserResource(Resource):
    @jwt_refresh_required
    def get(self, id):
        
        current_user = get_jwt_identity()
        user = User.get(id=id)
        

        if not user:
            return {"message" : "User does not exist"}, 404

        if user.id == current_user["id"]:
            
            return get_full_user(user.id), 200
        else:
            return user, 200

    @jwt_refresh_required
    def put(self, id):
        args = Arguments(request.json)
        args.dict("user", required=True)
        args.validate()

        current_user = get_jwt_identity()
        user = User.get(id=id)

        if not user or current_user["id"] != id:
            return {"message" : "You are not authorized to edit this profile"}, 401

        # Remove unuseable fields
        if "id" in args.user:
            del args.user["id"]
        if "images" in args.user:
            del args.user["images"]
        
        try:
            args.user["interests"] = args.user["interests"] if args.user["interests"] else ""
        
        except Exception:
            pass

        try:
            args.user["preferences"] = args.user["preferences"] if args.user["preferences"] else ""
        except Exception:
            pass
        user.update(args.user)

        try:
            #print(user.dump_fields())
            user.save()
            return {"message": "User updated"}, 200
        except Exception as e:
            return {"message": str(e)}, 400
