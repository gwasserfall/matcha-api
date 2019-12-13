from simplejson import JSONEncoder
from decimal import Decimal

from models import Model

class ModelEncoder(JSONEncoder):
    def default(self, obj):

        if isinstance(obj, Model):
            return dict(obj)

        if isinstance(obj, Decimal):
            return float(obj)

        return super(ModelEncoder, self).default(obj)
    