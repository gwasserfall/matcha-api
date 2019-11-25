import uuid
import hashlib
from pymysql.err import IntegrityError

from models.model import Model
from pprint import pprint

class User(Model):
	
	def __init__(self):
		super().__init__()

		self.id = ""
		self.fname = ""
		self.lname = ""
		self.email = ""
		self.username = ""
		self.passhash = ""
		self.bio = ""
		self.gender = ""
		self.age = ""
		self.longitude = ""
		self.latitude = ""
		self.fame = 0
		self.online = ""
		self.date_lastseen = ""

	def get(self, **kwargs):

		with self.db.cursor() as c:

			c.execute("""
				SELECT 
					id, fname, lname, email, username,
					bio, gender, age, longitude, latitude,
					fame, online, date_lastseen, date_joined,
					online
				FROM 
					users 
				WHERE 
					username=%s""", self.username)

			self.create(**c.fetchone())
		return True

	def create(self, **kwargs):
		for key, value in kwargs.items():
			if key == "password":
				self.passhash = self.hash_password(value)
				continue
			if key not in self.__dict__:
				return False
			else:
				# Set the value only if it exists
				value and setattr(self, key, value)
				print ("setting {} = {}".format(key, value))
		return self

	def insert_query(self, **kwargs):
		value_dict = self.to_dict()
		key = ", ".join(value_dict.keys())
		val = ", ".join(["%s"] * len(value_dict))
		
		return """
			INSERT INTO users
				({key})
			VALUES
				({value})
		""".format(key=key, value=val)

	def hash_password(self, password):
		salt = uuid.uuid4().hex
		return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
		
	def check_password(self, password):
		password, salt = hashed_password.split(':')
		return self.passhash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

	def to_dict(self):
		return {key : value for key, value in self.__dict__.items() 
			if key not in ["db", "id", "date_lastseen", "online"]
			and value
			}

	def insert(self):
		query = self.insert_query()
	
		try:
			with self.db.cursor() as c:
				c.execute(query, tuple(self.to_dict().values()))
				self.db.commit()

				self.get(username=self.username)
				return True
			
		except IntegrityError as e:
			print ("Duplicate entry here" + str(e))
			return False


	def keys(self):
		pass

	def __str__(self):
		return "<User {}>".format(self.username)

