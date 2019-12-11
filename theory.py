from collections.abc import MutableMapping
from datetime import datetime

import pymysql
import config
from datetime import datetime
from copy import deepcopy

import hashlib
import uuid

from pprint import pprint
from datetime import datetime

# Connect to the database
connection = pymysql.connect(**config.database)



class Field:
	def __init__(self, typeof=str, default=None, fmt="%Y-%m-%d", hidden=False):
		self.type = typeof
		self.hidden = hidden
		self.value = default
		self.fmt = fmt

	def __repr__(self):
		return "<{0}:{1}>".format(self.type.__name__, self.value)

	def deserialize(self):
		if self.type == datetime and self.value:
			return datetime.strptime(self.value, self.fmt)

		return self.type(self.value) if self.value else None

	def serialize(self, value):
		self.value = value



class Model(object):

	db = connection

	def __init__(self, _data={}, **kwargs):
		data = _data or kwargs
		self.fields = {}
		self.before_init(data)
		for k, v in self.__class__.__dict__.items():
			if isinstance(v, Field):
				self.fields[k] = deepcopy(v)
				if k in data.keys():
					self.fields[k].serialize(data[k])

	def __getattribute__(self, name):
		if name in ["__class__", "fields", "essential"]:
			return super(Model, self).__getattribute__(name)
		if name not in self.fields:
			return super(Model, self).__getattribute__(name)
		raise AttributeError

	def __getattr__(self, key):
		if key in self.fields:
			return self.fields[key].value
		raise AttributeError("Field not present {}".format(key))

	def __getitem__(self, key):
		if key in self.fields.keys():
			return self.fields[key].deserialize()
		else:
			return self.__dict__[key]

	def __setitem__(self, key, val):
		self.__setattr__(key, val)

	def __setattr__(self, key, val):
		if key is "fields":
			super(Model, self).__setattr__(key, val)
		else:
			if key in self.fields:
				self.fields[key].value = val
			else:
				raise AttributeError

	def __delitem__(self):
		pass

	def __repr__(self):
		return "<Model:{0} '{1}'>".format(self.__class__.__name__, self.id)

	def __len__(self):
		return len(self.fields)

	def __iter__(self):
		for k, v in self.fields.items():
			if not v.hidden:
				yield (k, v.value)

	def before_init(self, data):
		pass

	def save(self):
		columns = []
		values = []

		print("Saving")

		for name, field in self.fields.items():
			if name == "id" and not field.value:
				continue
			columns.append(name)
			values.append(field.deserialize())

		query = """
			REPLACE INTO users 
				({0})
			VALUES
				({1})
		""".format(", ".join(columns), ", ".join(["%s"] * len(values)))

		with self.db.cursor() as c:
			c.execute(query, tuple(values))
			self.db.commit()

	@classmethod
	def get(cls, **kwargs):
		if len(kwargs) > 1:
			return False
		key = next(iter(kwargs))
		val = kwargs[key]
		with cls.db.cursor() as c:
			c.execute("""
				SELECT 
					id, fname, lname, email, username, passhash,
					bio, gender, age, longitude, latitude,
					heat, date_lastseen, date_joined,
					online
				FROM 
					users 
				WHERE 
					{}=%s""".format(key), (val,))
			data = c.fetchone()
		return cls(data) if data else False


from pymysql.err import IntegrityError

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

	def before_init(self, data):

		if "password" in data:
			self.passhash.value = self.hash_password(data["password"])


	def hash_password(self, password):
		salt = uuid.uuid4().hex
		return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
		
	def check_password(self, password):
		_hash, salt = self.passhash.split(':')
		return _hash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

	def essential(self):
		return {
			"id" : self.id,
			"fname" : self.fname,
			"lname" : self.lname
		}




a = User({
    "id" : "1",
    "fname" : "firstname",
    "lname" : "lastname",
    "email" : "email@domain.tld",
    "username" : "username",
	"password" : "password",
    "bio" : "Biography in Markdown Syntax",
    "gender" : "female",
    "age" : 21,
    "longitude" : 40.714,
    "latitude" : -74.006,
    "heat" : 100,
    "date_joined" : "2018-01-01",
    "date_lastseen" : "2018-01-01"
})


a.age = 51

a.save()
