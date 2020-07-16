from pymysql.err import IntegrityError
from models import Model, Field

class   BlockRequest(Model):

    table_name = "block_requests"

    id = Field(int, modifiable=False)
    reporter_id = Field(int)
    reported_id = Field(int)
    reason = Field(str)
    reviewed = Field(bool, default=False)
    blocked = Field(bool, default=False)
    admin_comments = Field(str)

    