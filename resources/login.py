from flask import request

from flask import current_app as app
from datetime import datetime

from flask_restful import Resource
from flask_jwt_extended import (
    JWTManager,
                jwt_required,
                create_access_token,
                create_refresh_token,
    get_jwt_identity
)

from models.user import User, get_full_user

from twisted.python import log

from helpers import Arguments, is_email


class LoginResource(Resource):
    def post(self):
        """
        GET /v1/login
        """
        args = Arguments(request.json)
        args.string("username", required=True)
        args.string("password", required=True)
        args.validate()

        if is_email(args.username):
            user = User.get(email=args.username)
        else:
            user = User.get(username=args.username)

        if user and not user.email_verified:
            return {"message" : "Account not validated"}, 401
        elif user and user.check_password(args.password):
            identity = {
                    "id" : user.id,
                    "username" : user.username,
                    "email" : user.email}
            access_token = create_refresh_token(identity=identity)
            try:
                user.date_lastseen = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                user.save()
            except Exception as e:
                return {"message" : str(e)}, 401

            return {"access_token" : access_token, "user": get_full_user(user.id)}, 200

        else:
            return {"message" : "Failed to authenticate."}, 401
