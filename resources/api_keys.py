from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from helpers import Arguments, jwt_refresh_required

import config

class ApiKeysResource(Resource):
    @jwt_refresh_required
    def get(self):
        return {
            "google_maps" : config.maps_token,
            "ipstack" : config.ipstack
        }, 200