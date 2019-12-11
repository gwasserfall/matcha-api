from collections.abc import MutableMapping
from datetime import datetime

import pymysql
import config
from datetime import datetime
from copy import deepcopy

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



class Model(MutableMapping):

	db = connection

	def __init__(self, _data={}, **kwargs):
		data = _data or kwargs
		self.fields = {}
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
				yield k

	def save(self):
		columns = []
		values = []

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

