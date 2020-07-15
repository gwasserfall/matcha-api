from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

import requests

from helpers import Arguments, jwt_refresh_required

import config

class LocationResource(Resource):
    @jwt_refresh_required
    def get(self):
        r = requests.get("http://api.ipstack.com/{0}?access_key={1}".format(request.remote_addr, config.ipstack))

        return r.json(), 200

