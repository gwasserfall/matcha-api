from flask import request

from flask_restful import Resource
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)

from models.matches import Match

from helpers import Arguments, jwt_refresh_required

class RatingResource(Resource):
    @jwt_refresh_required
    def get(self, user_id):
        user = get_jwt_identity()

        match = Match.get(matcher_id=user["id"], matchee_id=user_id)
        if match:
            return match, 200
        else:
            return {"message": "No relationship found with this user."}, 404

    @jwt_refresh_required
    def put(self, user_id):
        user = get_jwt_identity()
        args = Arguments(request.json)
        args.integer("rating", required=True, min=1, max=5)
        args.validate()

        user = get_jwt_identity()

        has_match = Match.check_match(user["id"], user_id)

        if has_match and has_match["matched"]:
            match = Match.get(matcher_id=user["id"], matchee_id=user_id)
            try:
                match.rating = args.rating
                match.save()
                return {"message" : "Rating successful"}, 200
            except Exception as e:
                return {"message" : str(e)}, 500
        else:
            return {"message" : "You cannot rate this user, you are not matched."}, 400


    @jwt_refresh_required
    def delete(self, user_id):
        user = get_jwt_identity()
        match = Match.check_match(user["id"], user_id)

        return match or {"matched" : False, "liked" : False}, 200
