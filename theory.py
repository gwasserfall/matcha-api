# from pymysql.cursors import DictCursor

# from pprint import pprint

# from pypika import Query, Table, Field

# import pymysql

# database = {
# 	"host"			:'127.0.0.1',
# 	"user"			:'root',
# 	"password"		:'password',
# 	"db"			: 'matcha',
# 	"charset"		: 'utf8mb4',
# 	"cursorclass"	: DictCursor
# }

# # Connect to the database
# db = pymysql.connect(**database)

# class User():
# 	def __init__(self):
# 		self.db = db

# 	@staticmethod
# 	def filter(**kwargs):
# 		if kwargs:
# 			where = ", ".join(["{0}={1}".format(x,y) for x,y in kwargs.items()])
# 		else:
# 			where = None

# 		table = Table("users")

# 		with db.cursor() as c:
# 			q = Query.from_(table).select("*").where(table['username'].like("%ass"))

# 			print(q)

# 			c.execute(q.get_sql(quote_char=False))
# 			print(c._last_executed)
# 			pprint(c.fetchall())


# class ValidationError(Exception):
# 	pass

# class Column(dict):

# 	value = None

# 	def __init__(self, type_of, default=None, length=255):
# 		pass

# 	def __getattribute__(self, name):
# 		return "asd"

# 	def __getitem__(self, name):
# 		return "asd"

# 	def __setattr__(self, name, value):
# 		pass




# users = Users.getmany(username="%a%")

# user = Users.get(email="asda@asd.com")

# user = Users.create(**kwargs)

# user.name = "whatever"

# try:
# 	user.save()
# except ValidationException as e:
# 	return {"message" : e}, 401

# if user.delete():
# 	return {}, 201
# else:
# 	return {"message" : e}, 401

# from json import JSONEncoder
# import simplejson as json

# class A(dict):
#     pass


# a = A()

# a["asd"] = "asd"

# print(json.dumps(a))


from collections.abc import MutableMapping
from datetime import datetime
from pprint import pprint
import pymysql
import config
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



class Base(MutableMapping):

	def __init__(self):
		self.fields = {}
		for k, v in self.__class__.__dict__.items():
			if isinstance(v, Field):
				self.fields[k] = deepcopy(v)

	def __getattribute__(self, name):
		if name in ["__class__", "fields", "__dict__"]:
			return super(Base, self).__getattribute__(name)
		if name not in self.fields:
			return super(Base, self).__getattribute__(name)
		raise AttributeError

	def __getattr__(self, key):
		pprint(self.__dict__)
		if key in self.__dict__:
			print("HERE IT IS")

		if key in self.fields:
			return self.fields[key].value
		raise AttributeError("Field not present")

	def __getitem__(self, key):
		if key in self.fields.keys():
			return self.fields[key].deserialize()
		else:
			return self.__dict__[key]

	def __setitem__(self, key, val):
		self.__setattr__(key, val)


	def __setattr__(self, key, val):
		if key is "fields":
			super(Base, self).__setattr__(key, val)
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

	def func(self):
		print("asdasdasd")


class User(Base):
	
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



a = User()
b = User()

a.id = "1"

a.func()

