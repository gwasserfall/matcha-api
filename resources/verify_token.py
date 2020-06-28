from flask import request
from flask_restful import Resource, abort

from helpers import jwt_refresh_required


class VerifyTokenResource(Resource):
  @jwt_refresh_required
  def get(self, code):
    return {"message" : "Authenticated"}


    ## Seed data in database

    