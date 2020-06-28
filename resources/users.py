from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import get_jwt_identity
from helpers import jwt_refresh_required

from helpers.email import send_validation_email

from models.user import User
from models.validation import Validation

import secrets

from helpers import Arguments


class UserListResource(Resource):

    def get(self):

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
        
        current_user = get_jwt_identity() or {"id" : 1}
        user = User.get(id=id)

        if not user:
            return {"message" : "User does not exist"}, 404

        if user.id != current_user["id"]:
            return user, 200
        else:
            return user, 200
