from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from models.views import View
from helpers import Arguments, jwt_refresh_required

import traceback

class   ViewedByListResource(Resource):
    @jwt_refresh_required
    def get(self):
        current_user = get_jwt_identity()
        
        return View.get_viewed_by(self, user_id=current_user["id"])

class   ViewsListResource(Resource):
    @jwt_refresh_required
    def get(self):
        current_user = get_jwt_identity()

        return View.get_views(self, user_id=current_user["id"])

    @jwt_refresh_required
    def post(self):
        current_user = get_jwt_identity()

        args = Arguments(request.json)

        args.integer("viewee_id")
        args.validate()

        view = View(dict(args))
        view.viewer_id = current_user["id"]

        if View.get(viewer_id=current_user["id"], viewee_id=args.viewee_id):
            return {"message" : "Already viewed."}, 200
        try:
            view.save()
            return {"message" : "Viewed"}, 200
        except Exception as e:
            return {"message" : str(e)}, 500