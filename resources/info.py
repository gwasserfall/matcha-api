from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from models.images import Image
from helpers import Arguments, jwt_refresh_required
from helpers.genders import genders

import traceback

class GenderListResource(Resource):
    @jwt_refresh_required
    def get(self):
        return {"genders" : genders}, 200