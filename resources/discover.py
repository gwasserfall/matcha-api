from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from helpers import Arguments, jwt_refresh_required

from models.user import User

from database import pool

from datetime import datetime

class MatchList(object):
    def __init__(self, user, *args, **kwargs):
        self.fame_min = kwargs.get("fame_min", 0)
        self.fame_max = kwargs.get("fame_max", (user.heat or 3) + 1)
        self.age_min = kwargs.get("age_min", 18)
        self.age_max = kwargs.get("age_max", 99)
        self.tags_min = kwargs.get("tags_min", 1)
        self.user = user
        self.matches = []


    def filter_gender(self):
        preferences = self.user.preferences

        if not preferences:
            return

        for match in self.matches:

            if match["gender"] not in preferences:
                self.matches.remove(match)

    def filter_tags(self):
        for match in self.matches:
            
            # print("user interests", type(self.user.interests), self.user.interests)
            # print("user interests", type(match["interests"]), match["interests"])

            if not self.user.interests or not match["interests"]:
                match["tags"] = 0
            else:
                match["tags"] = len([x for x in self.user.interests if x in match["interests"]])
            
            if match["tags"] < self.tags_min:
                self.matches.remove(match)


    def deserialise(self):
        for match in self.matches:
            
            match["preferences"] = match["preferences"].split(",") if match["preferences"] else []
            match["interests"] = match["interests"].split(",") if match["interests"] else []
            


    def filter(self, data):
        self.matches = data

        self.deserialise()

        # for func in MatchList.__dict__.values():
        #     try:
        #         if "filter_" in func.__name__: 
        #             getattr(self, func.__name__)()
        #     except AttributeError as e:
        #         pass

        return self.matches



class DiscoveryListResource(Resource):
    @jwt_refresh_required
    def get(self):
        user = User.get(id=get_jwt_identity()["id"])

        matches = MatchList(user, **request.args)

        take = request.args.get("take", 20)
        skip = request.args.get("skip", 0)
        distance = request.args.get("distance", 20)
        
        try:
            take = int(take)
            skip = int(skip)
        except:
            skip = 0
            take = 20


        print("take is of type", type(take), take)
        print("skip is of type", type(skip), skip)

        connection = pool.get_conn()

        user.dump_fields()

        query = """
            SELECT
            users.id as id,
            fname,
            lname,
            bio,
            gender,
            dob,
            latitude,
            longitude,
            heat,
            preferences,
            interests,
            image64,
            image_type,
            CEIL(
                6371 * acos (
                cos ( radians(%s) )
                * cos( radians( latitude ) )
                * cos( radians( longitude ) - radians(%s) )
                + sin ( radians(%s) )
                * sin( radians( latitude ) )
                )
            ) AS distance
            FROM 
                users
            LEFT JOIN 
                images on images.id = (SELECT id FROM images where user_id=users.id ORDER BY is_primary DESC LIMIT 1)
            WHERE 
                users.id NOT IN (SELECT matchee_id FROM matches WHERE matcher_id=%s AND matchee_id=users.id)
                AND
                    %s NOT IN (SELECT reported_id FROM block_requests WHERE reporter_id=users.id AND blocked=1)
            HAVING distance <= %s
            ORDER BY distance ASC
            LIMIT %s, %s"""

        with connection.cursor() as c:
            c.execute(query, (user.latitude, user.longitude, user.latitude, user.id, user.id, distance, skip, take))
            pool.release(connection)

            return matches.filter(c.fetchall()), 200

        pool.release(connection)

        return [], 404