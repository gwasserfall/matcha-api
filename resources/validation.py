from flask import request
from flask_restful import Resource, abort

from models.validation import Validation

from models.user import User

from helpers.email import send_validation_email

class ValidationResource(Resource):

    def get(self, code):
        # Validate user email and delete entry
        if not code:
            return {"message" : "Your account could not be verified"}, 400

        validation = Validation.get(code=code)

        if validation:
            user = User.get(id=validation.user_id)
            user.email_verified = True
            user.save()
            validation.delete()
            return {"message" : "Your email has been verified"}, 200
        else:
            return {"message" : "Your account could not be verified"}, 400


class ValidationRetryResource(Resource):

    def post(self, email):
        # Resend user validation email here
        user = User.get(email=email)

        if user:
            validation = Validation.get(user_id=user.id)

            if validation:
                send_validation_email(user, validation.code)
            else:
                print("Validation not found for user")
        else:
            print("User not found", email)

        return {}, 200
