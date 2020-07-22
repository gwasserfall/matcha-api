
from database import pool
pool.init()
from models.user import User



user = User.get(id=501)

print(user.check_password("Password1"))