from models.user import User
from models.validation import Validation
import secrets

from flask import request
from flask_restful import Resource

from helpers import Arguments, is_email, jwt_refresh_required

from helpers.email import send_password_reset_email

class PasswordResetRequestResource(Resource):
  def post(self):
    args = Arguments(request.json)
    args.email("email", required=True)
    args.validate()

    user = User.get(email=args.email)

    if user:
      try:
          validation = Validation(user_id=user.id, code=secrets.token_urlsafe(256))
          validation.save()
          result = send_password_reset_email(user, validation.code)
          return {"message": result}, 200
      except Exception as e:
          return {"message" : str(e)}, 500
    return {"message" : "Action complete"}, 200

class PasswordChangeResource(Resource):
  def put(self):
    args = Arguments(request.json)
    args.string("code")
    args.string("user_id")
    args.string("previous_password")
    args.string("new_password", required=True)
    args.validate()

    if args.code != "None":
      print("Args code exists??")
      validation = Validation.get(code=args.code)
      if validation:
        user = User.get(id=validation.user_id)
        user.passhash = user.hash_password(args.new_password)
        user.save()
        return {"message": "Password updated"}, 200
      else:
        return {"message": "Unauthorised code"}, 401

    else:
      print("args.previous_password = ", args.previous_password)
      if args.user_id == "":
        return {"message": "User Id is required"}, 400

      if not args.previous_password:
        return {"message": "Previous password required"}, 400

      user = User.get(id=args.user_id)

      print(user)

      if user and user.check_password(args.previous_password):
        user.passhash = user.hash_password(args.new_password)
        user.save()
        return {"message": "Password updated"}, 200
      else:
        return {"message": "Your previous password is incorrect"}, 401