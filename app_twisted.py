import sys
import signal

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from autobahn.twisted.resource import WebSocketResource, WSGIRootResource

from flask_cors import CORS
from flask_restful import Resource, Api
from flask import Flask, render_template, request, jsonify, make_response
from flask_jwt_extended import JWTManager, decode_token

import config
# from models import connection
from helpers.model_encoder import ModelEncoder
from helpers import jwt_refresh_required
from sockets import get_server_factory, get_server_protocol

from resources import *

from models.user import User

app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SECRET_KEY'] = 'super-secret'
app.config['RESTFUL_JSON'] = {"cls": ModelEncoder, "encoding" : "utf-8"}

CORS(app)
jwt = JWTManager(app)
api = Api(app, prefix="/v1")

# TODO: Document for pair programming
api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/user/<string:id>")


api.add_resource(CurrentUserResource, "/user/current")
api.add_resource(LoginResource, "/login")

api.add_resource(ValidationResource, '/validate/<string:code>')
api.add_resource(ValidationRetryResource, '/validate/resubmit/<string:email>')

api.add_resource(VerifyTokenResource, "/verify-token")

api.add_resource(MatchListResource, "/matches")
api.add_resource(MatchResource, "/match/<int:user_id>")
api.add_resource(LikesListResource, "/likes")
api.add_resource(LikedByListResource, "/likes/liked-by")

api.add_resource(RatingResource, "/rating/<int:user_id>")

api.add_resource(PasswordResetRequestResource, "/reset-password-request")
api.add_resource(PasswordChangeResource, "/reset-password")

api.add_resource(ImageListResource, "/images")
api.add_resource(GenderListResource, "/info/genders")
api.add_resource(InterestsListResource, "/info/interests")

api.add_resource(DiscoveryListResource, "/discover")

api.add_resource(ApiKeysResource, "/api-keys")
api.add_resource(LocationResource, "/location")

api.add_resource(BlockRequestsListResource, "/block-requests")
api.add_resource(BlockRequestResource, "/block-request/<int:id>")
api.add_resource(BlocksResource, "/check-blocked/<string:username>")

api.add_resource(ViewsListResource, "/views")
api.add_resource(ViewedByListResource, "/views/viewed-by")

api.add_resource(UnmatchResource, "/unmatch/<int:user_id>")

import ast
from markdown import markdown
import os

import simplejson as json

@app.route("/test")
def test():
    user = User.get(id=1)
    response = make_response(json.dumps(user, default=ModelEncoder().default))
    response.headers['Content-Type'] = 'application/json'
    
    return response


@app.route("/")
def documentation():

    docs = []

    for py in [os.path.join("resources", x) for x in os.listdir("resources") if "__" not in x and x.endswith("py")]:
        with open(py) as f:
            code = ast.parse(f.read())

        for node in ast.walk(code):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                docstring = ast.get_docstring(node)
                if docstring:

                    endpoint = docstring.split("\n")[0]
                    md = "\n".join(docstring.split("\n")[1:])
                    
                    docs.append(
                      {
                        "endpoint" : endpoint,
                        "docstring" : markdown(md, extensions=['fenced_code', 'attr_list'])
                      }
                    )
    return render_template("api-docs.html", docs=docs)

from database import pool

from time import sleep

import sys


def shutdown_server():
    pool.destroy()
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    os.kill(-os.getpgid(os.getpid()), signal.SIGINT)


if __name__ == "__main__":
    debug = True if config.environment.lower() in ["dev", "development"] else False

    # Init the database pool
    pool.init()

    log.startLogging(sys.stdout)

    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)

    MatchaServerFactory = get_server_factory(app)
    MatchaServerProtocol = get_server_protocol(app)

    wsFactory = MatchaServerFactory("ws://0.0.0.0:5000")
    wsFactory.protocol = MatchaServerProtocol


    app.socks = wsFactory

    wsResource = WebSocketResource(wsFactory)


    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    site = Site(rootResource)

    reactor.addSystemEventTrigger('before', 'shutdown', shutdown_server)
    # signal.signal(signal.SIGINT, signal.default_int_handler)
    reactor.listenTCP(5000, site)
    reactor.run()
