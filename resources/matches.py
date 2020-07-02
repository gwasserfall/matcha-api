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

from twisted.python import log

from helpers import Arguments, is_email, jwt_refresh_required

class MatchListResource(Resource):
    @jwt_refresh_required
    def post(self):
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
        db = Match().db
        matches = []
        with db.cursor() as c:
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
                print("user")
                print(user)
                print("asd")
                
                matches.append(user)
        return matches


class MatchResource(Resource):
    @jwt_refresh_required
    def get(self, user_id):
        user = get_jwt_identity()
        match = Match.check_match(user["id"], user_id)

        return match or {"matched" : False, "liked" : False}, 200

	