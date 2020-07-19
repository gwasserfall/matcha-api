from flask import request

from flask import current_app as app

from flask_restful import Resource
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)

from models.matches import Match
from models.user import User
from models.images import Image
from models.block_request import BlockRequest

from twisted.python import log

from helpers import Arguments, is_email, jwt_refresh_required

class MatchListResource(Resource):
    @jwt_refresh_required
    def post(self):
        """
            Doc string to describe function
        """
        args = Arguments(request.json)
        args.string("matchee_id", required=True)
        args.validate()

        user = get_jwt_identity()

        images = Image.check_images(user_id=user["id"])

        if not images["has_images"]:
            return {"message" : "You cannot like a user if you have no profile images.", "no_photo" : True}, 401

        if Match.get(matchee_id=args.matchee_id, matcher_id=user["id"]):
            return {"message" : "Already liked."}, 200
        try:
            match = Match(matchee_id=args.matchee_id, matcher_id=user["id"])
            match.save()
        except Exception as e:
            return {"message" : str(e)}, 500
        return {"message" : "User liked."}, 200


    @jwt_refresh_required
    def get(self):
        """
        GET : /v1/matches (requires JWT)

        Get matches user profiles for the currently logged in user


        SUCCESS (200)

        ```json
            [
                {
                    "id": 1,
                }
            ]
        ```

        UNAUTHORISED (401)

        ```json

            {"message" : "Not authorised"}

        ```

        """
        temp = Match()
        connection = temp.pool.get_conn()
        matches = []
        with connection.cursor() as c:
            c.execute("""
            select * from users where id in (
                select matchee_id
                from matches
                    WHERE matcher_id in (
                        select matchee_id from matches where matchee_id = 102
                    ) and matchee_id in (
                        select matcher_id from matches where matcher_id != 102
                    )
                )
            """)
            for m in c.fetchall():
                user = User.get(id=m["id"])
                matches.append(user)
        return matches


class MatchResource(Resource):
    @jwt_refresh_required
    def get(self, user_id):
        user = get_jwt_identity()
        match = Match.check_match(user["id"], user_id)

        return match or {"matched" : False, "liked" : False}, 200

class   LikedByListResource(Resource):
    @jwt_refresh_required
    def get(self):
        current_user = get_jwt_identity()
        
        return Match.get_liked_by(self, user_id=current_user["id"])

class   LikesListResource(Resource):
    @jwt_refresh_required
    def get(self):
        current_user = get_jwt_identity()

        return Match.get_likes(self, user_id=current_user["id"])

class   UnmatchResource(Resource):
    @jwt_refresh_required
    def delete(self, user_id):
        current_user = get_jwt_identity()
        match = Match.check_match(current_user["id"], user_id)

        if match["liked"] or match["matched"]:
            my_like = Match.get(matcher_id=current_user["id"], matchee_id=user_id)
            their_like = Match.get(matcher_id=user_id, matchee_id=current_user["id"])
            
            if match["liked"] and match["matched"]:
                try:
                    my_like.delete()
                    their_like.delete()
                except Exception as e:
                    return {"message" : str(e)}, 500
            elif match["liked"] and not match["matched"]:
                try:
                    my_like.delete()
                except Exception as e:
                    return {"message" : str(e)}, 500

            try:
                my_block = {"reporter_id" : current_user["id"], "reported_id" : user_id, "reason" : "unmatch", "reviewed" : 1, "blocked" : 1, "admin_comments": "unmatch"}
                their_block = {"reporter_id" : user_id, "reported_id" : current_user["id"], "reason" : "unmatch", "reviewed" : 1, "blocked" : 1, "admin_comments": "unmatch"}
                block_them = BlockRequest(my_block)
                block_me = BlockRequest(their_block)
                block_me.save()
                block_them.save()
                return {"message" : "Successfully removed user relationship."}, 200
            except Exception as e:
                return {"message" : str(e)}, 500        
        else:
            return {"message" : "Unable to unlike/unmatch. No relationship exists with this user."}, 200
