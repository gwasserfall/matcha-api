from flask import request as req
from flask_restful import abort
from json import JSONEncoder
import re

class Arg(object):
	def __init__(self, name, _type, **kwargs):
		self.name = name
		self.type = _type
		self.required = kwargs.get("required", None)
		self.message = kwargs.get("message", None)
		self.min = kwargs.get("min", None)
		self.max = kwargs.get("max", None)
		self.enum = kwargs.get("enum", None)
		self.regex = kwargs.get("regex", None)
		self.email = kwargs.get("email", False)

	def __repr__(self):
		return "<Argument: '{}'>".format(self.name)

class Arguments(object):

	def __init__(self, request=None):
		self.arguments = []
		self.json = {}

		if not request:
			self.request = req.values
		else:
			self.request = request

	def string(self, name, **kwargs):
		self.arguments.append(Arg(name, str, **kwargs))

	def integer(self, name, **kwargs):
		self.arguments.append(Arg(name, int, **kwargs))

	def decimal(self, name, **kwargs):
		self.arguments.append(Arg(name, float, **kwargs))

	def enum(self, name, enum, **kwargs):
		self.arguments.append(Arg(name, list, enum=enum, **kwargs))

	def email(self, name, **kwargs):
		self.arguments.append(Arg(name, str, regex=r"[^@]+@[^@]+\.[^@]+", email=True, **kwargs))

	def validate(self):
		for arg in self.arguments:
			value = self.request.get(arg.name, None)

			# check required
			if arg.required and not value:
				abort(400, message=arg.message or "{} is required".format(arg.name))
				return False
			
			# type coercion
			try:
				if arg.type is not list:
					self.__setattr__(arg.name, arg.type(value))
			except ValueError as e:
				# abort here
				abort(400, message=arg.message or "{0} is not of type {1}".format(arg.name, arg.type.__name__))
				return False

			# Check min
			if arg.min:
				if arg.type in [int, float] and value < arg.min:
					abort(400, message=arg.message or "{} does not meet minimum length requirement".format(arg.name))
					return False
				if arg.type in [str] and len(value) < arg.min:
					abort(400, message=arg.message or "{} does not meet minimum length requirement".format(arg.name))
					return False

			# Check max
			if arg.max:
				if arg.type in [int, float] and value > arg.max:
					abort(400, message=arg.message or "{} does not meet maximum length requirement".format(arg.name))
					return False
				if arg.type in [str] and len(value) > arg.max:
					abort(400, message=arg.message or "{} does not meet maximum length requirement".format(arg.name))
					return False

			# Check regex only on string
			if arg.type is str and arg.regex and not re.match(arg.regex, value):
				if arg.email:
					arg.message="Email address is not valid"
				abort(400, message=arg.message or "{} failed regex match".format(arg.name))
				return False

			# Check enum
			if arg.enum and value not in arg.enum:
				abort(400, message=arg.message or "{} does not meet enum requirement".format(arg.name))
				return False				

			self.json[arg.name] = value

		return True

	def __iter__(self):
		for key, val in self.__dict__.items():
			if key not in ["json", "request", "arguments"]:
				yield (key, val)
