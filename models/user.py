import hashlib
import uuid

from pprint import pprint
from datetime import datetime

from pymysql.err import IntegrityError
from models import Model, Field

class User(Model):
	id = Field(int)
	fname = Field(str)
	lname = Field(str)
	email = Field(str)
	username = Field(str)
	passhash = Field(str, hidden=True)
	bio = Field(str)
	gender = Field(str)
	age = Field(int)
	longitude = Field(float)
	latitude = Field(float)
	heat = Field(int)
	online = Field(bool)
	date_lastseen = Field(datetime)

	def hash_password(self, password):
		salt = uuid.uuid4().hex
		return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
		
	def check_password(self, password):
		_hash, salt = self.passhash.split(':')
		return _hash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()





# class UserOld(Model):
	
# 	def __init__(self, **kwargs):

# 		self.id = kwargs.get("id", None)
# 		self.fname = kwargs.get("fname", None)
# 		self.lname = kwargs.get("lname", None)
# 		self.email = kwargs.get("email", None)
# 		self.username = kwargs.get("username", None)

# 		password = kwargs.get("password", None)

# 		if password:
# 			print("Creating a new user in code before database")
# 			self.passhash = self.hash_password(password)
# 		else:
# 			self.passhash = kwargs.get("passhash", None)
		
# 		self.bio = kwargs.get("bio", None)
# 		self.gender = kwargs.get("gender", None)
# 		self.age = kwargs.get("age", None)
# 		self.longitude = kwargs.get("longitude", None)
# 		self.latitude = kwargs.get("latitude", None)
# 		self.heat = kwargs.get("heat", None)
# 		self.online = kwargs.get("online", None)
# 		self.date_lastseen = None

# 	def filter(self, **kwargs):
# 		if kwargs:
# 			where = ", ".join(["{0}={1}" for x,y in kwargs.items()])
# 		else:
# 			where = ""

# 		with self.db.cursor() as c:
# 			c.execute("""
# 				SELECT * FROM users %s
# 			""", where)

# 	@classmethod
# 	def get(cls, **kwargs):

# 		if len(kwargs) > 1:
# 			return False

# 		key = next(iter(kwargs))
# 		val = kwargs[key]

# 		with cls.db.cursor() as c:

# 			c.execute("""
# 				SELECT 
# 					id, fname, lname, email, username, passhash,
# 					bio, gender, age, longitude, latitude,
# 					heat, date_lastseen, date_joined,
# 					online
# 				FROM 
# 					users 
# 				WHERE 
# 					{}=%s""".format(key), (val,))

# 			data = c.fetchone()
			
# 		return User(**data) if data else False

# 	def create(self, **kwargs):
# 		for key, value in kwargs.items():
# 			if key == "password":
# 				self.passhash = self.hash_password(value)
# 				continue
# 			if key not in self.__dict__:
# 				return False
# 			else:
# 				# Set the value only if it exists
# 				value and setattr(self, key, value)
# 				print ("setting {} = {}".format(key, value))
# 		return self

# 	def insert_query(self, **kwargs):
# 		value_dict = self._as_dict()
	
# 		key = ", ".join(value_dict.keys())
# 		val = ", ".join(["%s"] * len(value_dict))
		
# 		return """
# 			INSERT INTO users
# 				({key})
# 			VALUES
# 				({value})
# 		""".format(key=key, value=val)

# 	def hash_password(self, password):
# 		salt = uuid.uuid4().hex
# 		return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
		
# 	def check_password(self, password):
# 		_hash, salt = self.passhash.split(':')
# 		return _hash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

# 	def save(self):
# 		query = self.insert_query()
# 		print(query)
# 		try:
# 			with self.db.cursor() as c:
# 				c.execute(query, tuple(self._as_dict().values()))
# 				self.db.commit()

# 				fresh = self.get(username=self.username)
# 				for key, val in fresh._as_dict().items():
# 					self.__setattr__(key, val)
# 				return True
			
# 		except IntegrityError as e:
# 			print ("Duplicate entry here" + str(e))
# 			return False

# 	def __str__(self):
# 		return "<User {}>".format(self.username)

# 	def to_min_dict(self):
# 		return {key : value for key, value in self.__dict__.items() 
# 			if key in ["id", "bio", "username", "gender", "age", "heat"]}