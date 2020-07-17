import hashlib
import uuid

from datetime import datetime

from pymysql.err import IntegrityError
from models import Model, Field
from models.images import Image

from database import pool

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
    interests = Field(list)
    preferences = Field(list)
    deleted = Field(bool, modifiable=False, hidden=True)
    is_admin = Field(bool)

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
            connection = self.pool.get_conn()
            with connection.cursor() as c:
                c.execute("""
                        UPDATE {0} SET deleted = 1
                         WHERE id='{1}'
                """.format(self.table_name, self.id))
                connection.commit()
            self.pool.release(connection)
        else:
            raise Exception("User not in database")

    def destroy(self):
        if self.id:
            connection = self.pool.get_conn()
            with connection.cursor() as c:
                c.execute("DELETE FROM users WHERE id=%s", self.id)
                connection.commit()
            self.pool.release(connection)
        else:
            raise Exception("User not in database")

    @staticmethod
    def get_mini_users(matches):
        try:
            connection = pool.get_conn()

            query = ""





        except Exception as e:
            print("Exception in get_mini_users() method")
            print(e)
        finally:
            pool.release(connection)
            

def serialise_interests(interests):
    return ",".join(interests)

def deserialise_interests(interests):
    return [{"key" : x.strip().lower(), "value" : x.strip()}  for x in interests.split(",")]


def get_full_user(user_id):
    user = User.get(id=user_id)

    images = Image.get_many(user_id=user_id)

    # Get the images for that user
    user.append_field("images", Field(list, images))

    return user
