from pymysql.cursors import DictCursor
from dotenv import load_dotenv

import os

load_dotenv()

database = {
        "host"                          : os.getenv("DB_HOST"),
        "user"                          : os.getenv("DB_USERNAME"),
        "password"              : os.getenv("DB_PASSWORD"),
        "db"                                    : os.getenv("DB_DATABASE"),
        "charset"                       : 'utf8mb4',
        "cursorclass"   : DictCursor
}


environment = os.getenv("ENV")

frontend_uri = os.getenv("FRONTEND_URI")

send_in_blue = os.getenv("SEND_IN_BLUE")
