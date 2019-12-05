from pymysql.cursors import DictCursor

from pprint import pprint

from pypika import Query, Table, Field

import pymysql

database = {
	"host"			:'127.0.0.1',
	"user"			:'root',
	"password"		:'password',
	"db"			: 'matcha',
	"charset"		: 'utf8mb4',
	"cursorclass"	: DictCursor
}

# Connect to the database
db = pymysql.connect(**database)

class User():
	def __init__(self):
		self.db = db

	@staticmethod
	def filter(**kwargs):
		if kwargs:
			where = ", ".join(["{0}={1}".format(x,y) for x,y in kwargs.items()])
		else:
			where = None

		table = Table("users")

		with db.cursor() as c:
			q = Query.from_(table).select("*").where(table['username'].like("%ass"))

			print(q)

			c.execute(q.get_sql(quote_char=False))
			print(c._last_executed)
			pprint(c.fetchall())


class ValidationException(Exception):
	pass

class Column(dict):

	value = None

	def __init__(self, type_of, default=None, length=255):
		pass

	def __getattribute__(self, name):
		return "asd"

	def __getitem__(self, name):
		return "asd"

	def __setattr__(self, name, value):
		pass


c = Column("string")

print(c)