from datetime import datetime

msgPam = [
	{	
		"timestamp" : datetime(2019, 1, 1, 10, 30, 0),
		"message" : "Hey Jim, how are you?"
	},
	{	
		"timestamp" : datetime(2019, 1, 1, 10, 32, 0),
		"message" : "Need more pencils..."
	}
]

msgJim = [
	{	
		"timestamp" : datetime(2019, 1, 2, 10, 31, 0),
		"message" : "Hey Pamelaaaaaaaa, good you?"
	}
]

day = msgPam + msgJim
from pprint import pprint
day.sort(key=lambda x : x["timestamp"])
# pprint(day)

from itertools import groupby

a = groupby(day, 
	lambda x : 
		x["timestamp"].strftime("%Y-%m-%d")
		)

history = {}

for day in a:
	history[day[0]] = list(day[1])

pprint(history)





# from collections.abc import MutableMapping
# from datetime import datetime

# import pymysql
# import config
# from datetime import datetime
# from copy import deepcopy

# import hashlib
# import uuid

# from pprint import pprint
# from datetime import datetime

# # Connect to the database
# connection = pymysql.connect(**config.database)

# class FieldError(Exception):
# 	pass

# class Field:
# 	def __init__(self, 
# 				 typeof=str, 
# 				 default=None, 
# 				 fmt="%Y-%m-%d", 
# 				 hidden=False,
# 				 modifiable=True
# 				 ):
# 		self.modifiable = modifiable
# 		self.type = typeof
# 		self.hidden = hidden
# 		self.value = default
# 		self.fmt = fmt

# 	def __repr__(self):
# 		return "<{0}:{1}>".format(self.type.__name__, self.value)

# 	def deserialize(self):
# 		if self.type == datetime and self.value:
# 			return self.value.strftime(self.fmt)

# 		return self.value

# 	def serialize(self, value):
# 		self.value = value



# class Model(object):

# 	db = connection

# 	def __init__(self, _data={}, **kwargs):
# 		data = _data or kwargs
# 		self.fields = {}
# 		self.before_init(data)
# 		for k, v in self.__class__.__dict__.items():
# 			if isinstance(v, Field):
# 				self.fields[k] = deepcopy(v)
# 				if k in data.keys():
# 					self.fields[k].serialize(data[k])

# 	def __getattribute__(self, name):
# 		if name in ["__class__", "fields"]:
# 			return super(Model, self).__getattribute__(name)
# 		if name in self.fields:
# 			raise AttributeError
# 		return super(Model, self).__getattribute__(name)

# 	def __getattr__(self, key):
# 		if key in self.fields:
# 			return self.fields[key].value
# 		raise AttributeError("Field not present {}".format(key))

# 	def __getitem__(self, key):
# 		if key in self.fields.keys():
# 			return self.fields[key].deserialize()
# 		else:
# 			return self.__dict__[key]

# 	def __setitem__(self, key, val):
# 		self.__setattr__(key, val)

# 	def __setattr__(self, key, val):
# 		if key is "fields":
# 			super(Model, self).__setattr__(key, val)
# 		else:
# 			if key in self.fields:
# 				if self.fields[key].modifiable: 
# 					self.fields[key].value = val
# 				else:
# 					raise Exception("Cannot modify field '{}'".format(key))
# 			else:
# 				raise AttributeError("Field {0} does not exist in Model {1}".format(key, self.__class__.__name__))

# 	def __delitem__(self):
# 		pass

# 	def __repr__(self):
# 		return "<Model:{0} '{1}'>".format(self.__class__.__name__, self.id)

# 	def __len__(self):
# 		return len(self.fields)

# 	def __iter__(self):
# 		for k, v in self.fields.items():
# 			if not v.hidden:
# 				yield (k, v.value)

# 	def before_init(self, data):
# 		pass

# 	def save(self):
# 		columns = []
# 		values = []

# 		for name, field in self.fields.items():
# 			if name == "id" and not field.value:
# 				continue
# 			columns.append(name)
# 			try:
# 				values.append(field.deserialize())
# 			except TypeError as e:
# 				raise TypeError("Field {0} is not of type {1}".format(name, field.type.__name__))

# 		query = """
# 			REPLACE INTO users 
# 				({0})
# 			VALUES
# 				({1})
# 		""".format(", ".join(columns), ", ".join(["%s"] * len(values)))

# 		with self.db.cursor() as c:
# 			c.execute(query, tuple(values))
# 			self.db.commit()

# 	def update(self, _dict={}, **kwargs):
# 		data = _dict or kwargs

# 		if data:
# 			for k, v in data.items():
# 				self[k] = v
# 		else:
# 			raise Exception("Nothing to update")


# 	def delete(self):
		
# 		if self.id:
# 			with self.db.cursor() as c:
# 				c.execute("""
# 					DELETE FROM {0} WHERE id='{1}'
# 				""".format(self.table_name, self.id))
# 				self.db.commit()
# 		else:
# 			raise Exception("User not in database")

# 	@classmethod
# 	def get(cls, **kwargs):
# 		if len(kwargs) > 1:
# 			return False
# 		key = next(iter(kwargs))
# 		val = kwargs[key]

# 		temp = cls()
# 		with temp.db.cursor() as c:
# 			c.execute("""
# 				SELECT 
# 					{fields}
# 				FROM 
# 					{table} 
# 				WHERE   {cond}=%s""".format(
# 						fields = ", ".join(temp.fields.keys()),
# 						table = cls.table_name,
# 						cond = key), (val,))
			
# 			data = c.fetchone()

# 		return cls(data) if data else False

# from pymysql.err import IntegrityError

# class User(Model):

# 	table_name = "users"

# 	id = Field(int, modifiable=False)
# 	fname = Field(str)
# 	lname = Field(str)
# 	email = Field(str)
# 	username = Field(str)
# 	passhash = Field(str, hidden=True)
# 	bio = Field(str)
# 	gender = Field(str)
# 	dob = Field(datetime)
# 	longitude = Field(float)
# 	latitude = Field(float)
# 	heat = Field(int)
# 	online = Field(bool)
# 	date_lastseen = Field(datetime)
# 	deleted = Field(bool, modifiable=False)

# 	def before_init(self, data):
# 		if "password" in data:
# 			self.passhash.value = self.hash_password(data["password"])

# 	def hash_password(self, password):
# 		salt = uuid.uuid4().hex
# 		return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
		
# 	def check_password(self, password):
# 		_hash, salt = self.passhash.split(':')
# 		return _hash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

# 	def delete(self):

# 		if self.id:
# 			with self.db.cursor() as c:
# 				c.execute("""
# 					UPDATE {0} SET deleted = 1
# 					 WHERE id='{1}'
# 				""".format(self.table_name, self.id))
# 				self.db.commit()
# 		else:
# 			raise Exception("User not in database")

# 	def essential(self):
# 		return {
# 			"id" : self.id,
# 			"fname" : self.fname,
# 			"lname" : self.lname
# 		}

# # a = User({
# #     "id" : "1",
# #     "fname" : "firstname",
# #     "lname" : "lastname",
# #     "email" : "email@domain.tld",
# #     "username" : "username",
# #     "password" : "password",
# #     "bio" : "Biography in Markdown Syntax",
# #     "gender" : "female",
# #     "dob" : "2018-01-01",
# #     "longitude" : 40.714,
# #     "latitude" : -74.006,
# #     "heat" : 100,
# #     "date_joined" : "2018-01-01",
# #     "date_lastseen" : "2018-01-01"
# # })

# #a.save()


# b = User.get(id=1)

# b.update(fname=False)

# pprint(dict(b))

# b.save()

# # if b:
# # 	print ("OKS")