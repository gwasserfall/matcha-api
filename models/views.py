from datetime import datetime

from pymysql.err import IntegrityError
from models import Model, Field

class View(Model):

    table_name = "views"

    id = Field(int, modifiable=False)
    date = Field(datetime, default=datetime.now())
    viewer_id = Field(int)
    viewee_id = Field(int)

    @staticmethod
    def get_viewed_by(self, user_id):
        pass

    @staticmethod
    def get_views(self, user_id):
        pass