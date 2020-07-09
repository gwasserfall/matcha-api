from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from models.images import Image
from helpers import Arguments, jwt_refresh_required

import traceback

class ImageListResource(Resource):
    @jwt_refresh_required
    def put(self):
        args = Arguments(request.json)
        args.integer("id")
        args.boolean("is_primary")
        args.string("image64", required=True)
        args.string("image_type", required=True)
        args.validate()

        user = get_jwt_identity()

        data = dict(args)
        data["user_id"] = user["id"]

        image = Image.get(id=data.get("id", None), user_id=user["id"])

        if image:
            image.image64 = data["image64"]
            image.image_type = data["image_type"]
            image.is_primary = data.get("is_primary", False)
        else:
            image = Image(data)

        try:
            image.save()
            return {"message" : "Image saved"}, 200
        except Exception as e:
            return {"message" : str(e)}, 400

class ImageResource(Resource):
    def get(self, id):
        image = Image.get(id=id)
        if image:
            return image, 200
        return {"message" : "Image not found"}, 404