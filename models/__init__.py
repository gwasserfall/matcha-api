from collections.abc import MutableMapping
from datetime import datetime

import pymysql
import config

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


class Model(MutableMapping):
	
	db = connection
	fields = {}

	def __init__(self, _data={}, **kwargs):
		print("MODEL HAS CALLED INIT")
		data = _data or kwargs
		for k, v in self.__class__.__dict__.items():
			if isinstance(v, Field):
				if k in data.keys():
					v.value = data[k]
				self.fields[k] = v

	def __delitem__(self):
		print("__delitem__")
		pass

	def __iter__(self):
		for field in Model.fields:
			if not Model.fields[field].hidden:
				yield field

	def __len__(self):
		return len(self.fields)

	def __getitem__(self, key):
		# print("__getitem__({})".format(key))
		if key in self.fields.keys():
			return self.fields[key].deserialize()
		else:
			raise AttributeError("{0} model has no '{1}' field".format(self.__class__.__name__, key))

	def __setitem__(self, key, val):
		self.__setattr__(key, val)

	def __getattribute__(self, name):
		# print ("__getattribute__({})".format(name))

		if name is not "field" and name in Model.fields.keys():
			return Model.fields[name].deserialize()
		return super(Model, self).__getattribute__(name)

	def __setattr__(self, key, val):
		
		if key in self.fields.keys():
			self.fields[key].value = val
		else:
			raise AttributeError("{0} model has no '{1}' field".format(self.__class__.__name__, key))

	def __repr__(self):
		return "<Model:{0} '{1}'>".format(self.__class__.__name__, self.id)

	def save(self):
		pass

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
			print("DATA HERE::", data)
		return cls(data) if data else False

