from datetime import datetime

from pymysql.err import IntegrityError
from models import Model, Field
from database import pool

class Match(Model):

    table_name = "matches"

    id = Field(int, modifiable=False)
    date = Field(datetime, default=datetime.now())
    matchee_id = Field(int)
    matcher_id = Field(int)
    rating = Field(int, default=0)

    @staticmethod
    def get_likes(self, user_id):
        connection = pool.get_conn()
        with connection.cursor() as c:
            date_format = '%e %b %Y'
            c.execute("""
                SELECT
                    m.id, 
                    m.matcher_id,
                    m.matchee_id, 
                    u.fname AS 'matchee_first_name', 
                    u.lname AS 'matchee_last_name',
                    u.username AS 'matchee_username',
                    DATE_FORMAT(m.date, %s) as date
                FROM matches m
                INNER JOIN users u
                ON m.matchee_id = u.id
                WHERE m.matcher_id = %s
            """, (date_format, user_id,))
            pool.release(connection)
            return c.fetchall()
        pool.release(connection)
        return None

    @staticmethod
    def get_liked_by(self, user_id):
        connection = pool.get_conn()
        with connection.cursor() as c:
            date_format = '%e %b %Y'
            c.execute("""
                SELECT
                    m.id, 
                    m.matcher_id,
                    u.fname AS 'matcher_first_name', 
                    u.lname AS 'matcher_last_name',
                    u.username AS 'matcher_username',
                    m.matchee_id,
                    DATE_FORMAT(m.date, %s) as date
                FROM matches m
                INNER JOIN users u
                ON m.matcher_id = u.id
                WHERE m.matchee_id = %s
            """, (date_format, user_id,))
            pool.release(connection)
            return c.fetchall()
        pool.release(connection)
        return None

    @classmethod
    def check_match(cls, matcher_id, matchee_id):
        temp = cls()

        connection = temp.pool.get_conn()
        with connection.cursor() as c:
            c.execute("""
              SELECT
                EXISTS(SELECT * FROM matches WHERE matcher_id=%s and matchee_id=%s) as liked,
                EXISTS(SELECT * FROM matches WHERE matcher_id=%s and matchee_id=%s and liked=1) as matched
              from matches
            """, [matcher_id, matchee_id, matchee_id, matcher_id])
            temp.pool.release(connection)
            return c.fetchone()
        temp.pool.release(connection)
        return None
