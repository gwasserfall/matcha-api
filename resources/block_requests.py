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

class   BlocksResource(Resource):
    @jwt_refresh_required
    def get(self, username):
        current_user = get_jwt_identity()
        blocked = BlockRequest.check_blocked(current_user["id"], username)

        print(blocked)

        return blocked or {"blocked_them" : False, "blocked_them" : False}, 200

class   BlockRequestsListResource(Resource):
    @jwt_refresh_required
    def get(self):
        current_user = get_jwt_identity()
        user = User.get(id=current_user["id"])

        if not user.is_admin:
            return {"message" : "You do not have admin access."}, 401
        else:
            return BlockRequest.get_all(), 200

    @jwt_refresh_required
    def post(self):
        current_user = get_jwt_identity()

        args = Arguments(request.json)
        args.integer("reported_id")
        args.string("reason")
        args.validate()

        block_request = BlockRequest(dict(args))
        block_request.reporter_id = current_user["id"]

        try:
            block_request.save()
            return {"message" : "User reported."}, 200
        except Exception as e:
            return {"message" : str(e)}, 400

class   BlockRequestResource(Resource):

    @jwt_refresh_required
    def put(self, id):
        current_user = get_jwt_identity()
        user = User.get(id=current_user["id"])

        if not user.is_admin:
            return {"message" : "You are not authorised to review block requests"}, 401
        else:
            args = Arguments(request.json)
            args.boolean("blocked")
            args.string("admin_comments")
            args.validate()

            data = dict(args)
            data["id"] = id

            block_request = BlockRequest.get(id=data.get("id", None))

            if block_request:
                block_request.reviewed = True
                block_request.blocked = data["blocked"]
                if data["admin_comments"]:
                    block_request.admin_comments = data["admin_comments"]

                try:
                    block_request.save()
                    msg = "Request reviewed. User blocked." if block_request.blocked == 1 else "Request reviewed. User NOT blocked."
                    return {"message" : "{}".format(msg)}, 200
                except Exception as e:
                    return {"message" : str(e)}, 400
            else:
                return {"messgae" : "The block request you are trying to update does not exist"}, 400

