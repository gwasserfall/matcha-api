from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from helpers import Arguments, jwt_refresh_required

from models.user import User

from database import pool


class DiscoveryListResource(Resource):
    #@jwt_refresh_required
    def get(self):
        # user = get_jwt_identity() or {"id" : 1}

        connection = pool.get_conn()

        user = User.get(id=1)

        query = """
            SELECT
            *, (
                6371 * acos (
                cos ( radians(%s) )
                * cos( radians( latitude ) )
                * cos( radians( longitude ) - radians(%s) )
                + sin ( radians(%s) )
                * sin( radians( latitude ) )
                )
            ) AS distance
            FROM users
            HAVING distance < 15
            ORDER BY distance
            LIMIT 0 , 20"""


        with connection.cursor() as c:
            c.execute(query, (user.latitude, user.longitude, user.latitude))
            return c.fetchall(), 200

        pool.release(connection)

        return {"billy" : "asdasd"}, 200