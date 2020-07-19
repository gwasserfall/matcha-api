from flask import request

from flask_restful import Resource

from models.matches import Match
from models.user import User

from twisted.python import log

from flask_jwt_extended import get_jwt_identity

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

        if Match.get(matchee_id=args.matchee_id, matcher_id=user["id"]):
            return {"message" : "Already matched"}, 200
        try:
            match = Match(matchee_id=args.matchee_id, matcher_id=user["id"])
            match.save()
        except Exception as e:
            return {"message" : str(e)}, 500
        return {"message" : "Matched"}, 200



    @jwt_refresh_required
    def get(self):
        """
        GET : /v1/matches (requires JWT)
        """

        current_user = get_jwt_identity()

        temp = Match()
        connection = temp.pool.get_conn()
        matches = []
        with connection.cursor() as c:
            c.execute("""
            SELECT * FROM users WHERE id IN (
                SELECT 
                    rhs.matcher_id 
                FROM 
                    matches lhs 
                LEFT JOIN 
                    matches rhs ON lhs.matcher_id = %s
                WHERE rhs.matchee_id = %s AND lhs.matchee_id = rhs.matcher_id
            )
            """, (current_user["id"], current_user["id"]))
            for m in c.fetchall():
                user = User.get(id=m["id"])
                user.get_primary_image()
                matches.append(user)

        temp.pool.release(connection)
        return matches, 200


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
