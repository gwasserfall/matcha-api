from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import get_jwt_identity
from helpers import jwt_refresh_required

from helpers.genders import genders
from helpers.email import send_validation_email

from models.user import User, get_full_user
from models.validation import Validation
from models.block_request import BlockRequest


from helpers import Arguments

import traceback

class   BlockRequestsListResource(Resource):
    @jwt_refresh_required
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)


        user = User.get(id=current_user["id"])
        print(user)


        return {}, 200



        if not user.is_admin:
            return {"message" : "You do not have admin access."}, 401
        else:
            print(BlockRequest.get())
            return {}, 200

    @jwt_refresh_required
    def post(self):
        pass

class   BlockRequestResource(Resource):

    @jwt_refresh_required
    def put(self, id):
        pass