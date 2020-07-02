from simplejson import JSONEncoder
from datetime import datetime, date
from decimal import Decimal

from models import Model

class ModelEncoder(JSONEncoder):
    def default(self, obj):

        print("JSON Encoding", type(obj), obj)

        if isinstance(obj, Model):
            return dict(obj)

        if isinstance(obj, datetime):
            return obj.replace(microsecond=0).isoformat()

        if isinstance(obj, date):
            return obj.isoformat()

        if isinstance(obj, Decimal):
            return float(obj)

        return super(ModelEncoder, self).default(obj)