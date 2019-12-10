import pymysql
import config
from datetime import datetime

# Connect to the database
connection = pymysql.connect(**config.database)

class Model(object):
	db = connection
	
	def save(self):
		with self.db.cursor() as c:
			pass

	def __iter__(self):
		for key, value in self.__dict__.items():

			if type(value) == datetime:
				yield (key, datetime.strftime(value, "%Y-%m-%d"))

			elif key not in ["db", "passhash"]:
				yield (key, value)

	def _as_dict(self):
		return {key : value for key, value in self.__dict__.items() 
			if key not in ["db"]}