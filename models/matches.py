from datetime import datetime

from pymysql.err import IntegrityError
from models import Model, Field

class Match(Model):

    table_name = "matches"

    id = Field(int, modifiable=False)
    date = Field(datetime, default=datetime.now())
    matchee_id = Field(int)
    matcher_id = Field(int)
    rating = Field(int, default=0)

    @classmethod
    def check_match(cls, matcher_id, matchee_id):
        temp = cls()

        with temp.db.cursor() as c:
            c.execute("""
              SELECT
                EXISTS(SELECT * FROM matches WHERE matcher_id=%s and matchee_id=%s) as liked,
                EXISTS(SELECT * FROM matches WHERE matcher_id=%s and matchee_id=%s and liked=1) as matched
              from matches
            """, [matcher_id, matchee_id, matchee_id, matcher_id])
            return c.fetchone()
        return None
