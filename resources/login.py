from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity
)

from models.user import User

from helpers import Arguments, is_email


class LoginResource(Resource):
	def post(self):
		args = Arguments(request.json)
		args.string("username", required=True)
		args.string("password", required=True)
		args.validate()

		if is_email(args.username):
			user = User.get(email=args.username)
		else:
			user = User.get(username=args.username)

		if user and user.check_password(args.password):
<<<<<<< HEAD
			identity = {
				"id" : user.id,
				"username" : user.username,
				"email" : user.email}
			access_token = create_refresh_token(identity=identity)
=======
			access_token = create_access_token(identity=args.username. wnknalsd=False)
>>>>>>> 638dfa7e91921ee8988c096fec3fd86cf57ce21a
			return {"access_token" : access_token}, 200

		else:
			return {"message" : "Failed to authenticate"}, 401	