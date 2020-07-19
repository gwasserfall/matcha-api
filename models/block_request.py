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
                    u1.fname AS 'reporter_first_name', 
                    u1.lname AS 'reporter_last_name', 
                    u1.username AS 'reporter_username',
                    b.reported_id,
                    u2.fname AS 'reported_first_name', 
                    u2.lname AS 'reported_last_name',
                    u2.username AS 'reported_username',
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

    @classmethod
    def check_blocked(cls, reporter_id, reported_username):
        temp = cls()

        connection = temp.pool.get_conn()
        with connection.cursor() as c:
            c.execute("""
            SELECT
                EXISTS(SELECT * FROM block_requests WHERE reporter_id=%s AND reported_id=(SELECT id FROM users WHERE username=%s) AND blocked=1) as blocked_them,
                EXISTS(SELECT * FROM block_requests WHERE reporter_id=(SELECT id FROM users WHERE username=%s) AND reported_id=%s AND blocked=1) as blocked_me              
            from block_requests
            """, (reporter_id, reported_username, reported_username, reporter_id))
            temp.pool.release(connection)
            return c.fetchone()
        temp.pool.release(connection)
        return None