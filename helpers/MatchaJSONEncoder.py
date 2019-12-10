from json import JSONEncoder
from decimal import Decimal


class MatchaJSONEncoder(JSONEncoder):
    def default(self, obj):
        print(obj)

        if isinstance(obj, Decimal):
            return float(obj)

        super().default(obj)
    