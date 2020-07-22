from models import Model, Field
from models.images import Image
from datetime import datetime

from database import pool

class Message(Model):
    table_name = "messages"

    id = Field(int, modifiable=False)
    to_id = Field(int)
    from_id = Field(int)
    timestamp = Field(datetime, default=datetime.now())
    message = Field(str)
    seen = Field(bool)
