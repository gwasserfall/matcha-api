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
from pprint import pprint
import inspect

def get_user_attributes(cls):
    boring = dir(MutableMapping)
    return [item
            for item in cls.__dict__.keys()
            if item[0] not in boring]


class Field:
	def __init__(self, default=None):
		self.value = default

	def __repr__(self):
		return "<Field>"


class Model(MutableMapping):

	db = "Database"

	def __delitem__(self):
		print("__delitem__")
		pass

	def __iter__(self):
		print("__iter__")
		pass

	def __len__(self):
		print("__len__")
		pass

	def __getitem__(self):
		print("__getitem__")
		pass

	def __setitem__(self, key, val):
		print("__setitem__", key, val)
		pass

	# def __getattribute__(self, key):
	# 	print("__getattribute__", key)

	def __setattr__(self, key, val):
		if key in self.__class__.__dict__.keys():
			self.__dict__[key] = val
		else:
			raise Exception("Not a field of this class")


	def __repr__(self):
		return "<Model:{0} 'name'>".format(self.__class__.__name__)



class User(Model):

	id = Field()
	username = Field()
	name2 = ""
	name3 = ""
	name4 = ""
	name5 = ""

	pass

b = User()

print("\n")
print(b)
b.id = 1

