from flask_jwt_extended.exceptions import *
from flask_restful import abort
from functools import wraps
from flask_jwt_extended import verify_jwt_refresh_token_in_request

from flask import request

def jwt_refresh_required(fn):
    """
        Overriding JWT wrapper to get cutsom message

    A decorator to protect a Flask endpoint.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid access token before allowing the endpoint to be called. This
    does not check the freshness of the access token.

    See also: :func:`~flask_jwt_extended.fresh_jwt_required`
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_refresh_token_in_request()
        except Exception as e:
            abort(401, message=str(e))
        return fn(*args, **kwargs)
    return wrapper
