import pymysql
import config

# Connect to the database
connection = pymysql.connect(**config.database)

class Model(object):
	def __init__(self):
		self.db = connection