from pymysql.cursors import DictCursor
from dotenv import load_dotenv

import os

load_dotenv()

database = {
	"host"			: os.getenv("DB_HOST"),
	"user"			: os.getenv("DB_USERNAME"),
	"password"		: os.getenv("DB_PASSWORD"),
	"db"			: os.getenv("DB_DATABASE"),
	"charset"		: 'utf8mb4',
	"cursorclass"	: DictCursor
}

print(database)