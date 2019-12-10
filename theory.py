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
		print("__getitem__({})".format(key))
		if key in self.fields.keys():
			return self.fields[key].deserialize()
		else:
			raise AttributeError("{0} model has no '{1}' field".format(self.__class__.__name__, key))

	def __setitem__(self, key, val):
		self.__setattr__(key, val)

	def __getattribute__(self, name):
		print ("__getattribute__({})".format(name))

		if name is "field" and name in Model.fields.keys():
			return Model.fields[name].deserialize()
		return super(Model, self).__getattribute__(name)

	def __setattr__(self, key, val):
		
		if key in self.fields.keys():
			self.fields[key].value = val
		else:
			raise AttributeError("{0} model has no '{1}' field".format(self.__class__.__name__, key))

	def __repr__(self):
		return "<Model:{0} '{1}'>".format(self.__class__.__name__, self.id)


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


a = User({"id" : 1})


pprint(dict(a))


connection.close()