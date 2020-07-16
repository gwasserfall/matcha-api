from pymysql.err import IntegrityError
from models import Model, Field
from database import pool

class   BlockRequest(Model):

    table_name = "block_requests"

    id = Field(int, modifiable=False)
    reporter_id = Field(int)
    reported_id = Field(int)
    reason = Field(str)
    reviewed = Field(bool, default=False)
    blocked = Field(bool, default=False)
    admin_comments = Field(str)

    @staticmethod
    def get_all():
        connection = pool.get_conn()
        with connection.cursor() as c:
            c.execute("""
                SELECT
                    b.id, 
                    b.reporter_id,
                    u1.fname AS 'reporter_firstname', 
                    u1.lname AS 'reporter_lastname', 
                    b.reported_id,
                    u2.fname AS 'reported_firstname', 
                    u2.lname AS 'reported_lastname',
                    b.reason, 
                    b.reviewed, 
                    b.blocked, 
                    b.admin_comments 
                FROM block_requests b
                INNER JOIN users u1
                ON b.reporter_id = u1.id
                INNER JOIN users u2
                ON b.reported_id = u2.id
                WHERE b.reviewed = 0
            """)
            pool.release(connection)
            return c.fetchall()
        pool.release(connection)
        return None
