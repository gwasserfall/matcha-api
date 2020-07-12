from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from models.images import Image
from helpers import Arguments, jwt_refresh_required
from helpers.genders import genders

from database import pool

class GenderListResource(Resource):
    @jwt_refresh_required
    def get(self):
        return {"genders" : genders}, 200

class InterestsListResource(Resource):
    @jwt_refresh_required
    def get(self):
        interests = ""
        connection = pool.get_conn()
        with connection.cursor() as c:
            c.execute("""SELECT GROUP_CONCAT(interests SEPARATOR ',') AS interests FROM users WHERE interests <> ''""")
            interests = c.fetchone().get("interests", "")
        pool.release(connection)
        return {"interests" : interests.split(",") if interests != "" else []}, 200