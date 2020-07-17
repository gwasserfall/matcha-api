from datetime import datetime

from pymysql.err import IntegrityError
from models import Model, Field
from database import pool

class View(Model):

    table_name = "views"

    id = Field(int, modifiable=False)
    date = Field(datetime, default=datetime.now())
    viewer_id = Field(int)
    viewee_id = Field(int)

    @staticmethod
    def get_viewed_by(self, user_id):
        connection = pool.get_conn()
        with connection.cursor() as c:
            date_format = '%e %b %Y'
            c.execute("""
                SELECT
                    v.id, 
                    v.viewer_id,
                    u.fname AS 'viewer_first_name', 
                    u.lname AS 'viewer_last_name',
                    v.viewee_id,
                    DATE_FORMAT(v.date, %s) as date
                FROM views v
                INNER JOIN users u
                ON v.viewer_id = u.id
                WHERE v.viewee_id = %s
            """, (date_format, user_id,))
            pool.release(connection)
            return c.fetchall()
        pool.release(connection)
        return None

    @staticmethod
    def get_views(self, user_id):
        connection = pool.get_conn()
        with connection.cursor() as c:
            date_format = '%e %b %Y'
            c.execute("""
                SELECT
                    v.id, 
                    v.viewer_id,
                    v.viewee_id, 
                    u.fname AS 'viewee_first_name', 
                    u.lname AS 'viewee_last_name',
                    DATE_FORMAT(v.date, %s) as date
                FROM views v
                INNER JOIN users u
                ON v.viewee_id = u.id
                WHERE v.viewer_id = %s
            """, (date_format, user_id,))
            pool.release(connection)
            return c.fetchall()
        pool.release(connection)
        return None