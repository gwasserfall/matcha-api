from simplejson import JSONEncoder
from decimal import Decimal

from models import Model

class MatchaJSONEncoder(JSONEncoder):
    def default(self, obj):

        if isinstance(obj, Model):
            return dict(obj)

        if isinstance(obj, Decimal):
            return float(obj)

        return super(MatchaJSONEncoder, self).default(obj)
    