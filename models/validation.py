from pymysql.err import IntegrityError
from models import Model, Field

class Validation(Model):
    table_name = "validations"

    id = Field(int, modifiable=False)
    user_id = Field(int)
    code = Field(str)
