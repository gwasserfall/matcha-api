from flask_jwt_extended.exceptions import *
from flask_restful import abort
from functools import wraps
from flask_jwt_extended import verify_jwt_refresh_token_in_request
from flask_socketio import ConnectionRefusedError

from pprint import pprint
from flask import request

def jwt_required_socket(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print("Checking for jwt token in socket")
        try:
            verify_jwt_refresh_token_in_request()
            kwargs["authenticated"] = True
            print("FOUND TOKEN")
        except Exception as e:
            print("TOKEN NOT FOUND")
            kwargs["authenticated"] = False
        return fn(*args, **kwargs)
    return wrapper