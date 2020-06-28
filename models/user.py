import hashlib
import uuid

from datetime import datetime

from pymysql.err import IntegrityError
from models import Model, Field

class User(Model):
	
	table_name = "users"

	id = Field(int, modifiable=False)
	fname = Field(str)
	lname = Field(str)
	email = Field(str)
	username = Field(str)
	passhash = Field(str, hidden=True)
	email_verified = Field(bool, default=False)
	bio = Field(str)
	gender = Field(str)
	dob = Field(datetime)
	longitude = Field(float)
	latitude = Field(float)
	heat = Field(int)
	online = Field(bool)
	date_lastseen = Field(datetime)
	deleted = Field(bool, modifiable=False, hidden=True)

	def before_init(self, data):
		if "password" in data:
			self.passhash.value = self.hash_password(data["password"])

	def hash_password(self, password):
		salt = uuid.uuid4().hex
		return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
		
	def check_password(self, password):
		_hash, salt = self.passhash.split(':')
		return _hash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

	def delete(self):

		if self.id:
			with self.db.cursor() as c:
				c.execute("""
					UPDATE {0} SET deleted = 1
					 WHERE id='{1}'
				""".format(self.table_name, self.id))
				self.db.commit()
		else:
			raise Exception("User not in database")

	def destroy(self):
		if self.id:
			with self.db.cursor() as c:
				c.execute("DELETE FROM users WHERE id=%s", self.id)
				self.db.commit()
		else:
			raise Exception("User not in database")


	def essential(self):
		return {
			"id" : self.id,
			"fname" : self.fname,
			"lname" : self.lname
		}
