import pymysql
import config

# Connect to the database
connection = pymysql.connect(**config.database)

class Model(object):
	db = connection
	
	def save(self):
		with self.db.cursor() as c:
			pass