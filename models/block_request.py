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
    def get():
        connection = pool.get_conn()
        with connection.cursor() as c:
            c.execute("""
                SELECT 
                    id, 
                    reported_id, 
                    reporter_id, 
                    reason, 
                    reviewed, 
                    blocked, 
                    admin_comments 
                FROM block_requests 
                WHERE reviewed = 0
            """)
            pool.release(connection)
            return c.fetchall()
        pool.release(connection)
        return None
