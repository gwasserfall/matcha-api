from database import pool
from random import random, randint

import requests


pool.init()



## Clear the users table
# connection = pool.get_conn()

# with connection.cursor() as c:
#     c.execute("DELETE FROM users WHERE id <> 1")
#     c.execute("ALTER TABLE users AUTO_INCREMENT = 2")


from datetime import datetime

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def get_images():
    randint(0,5)

def pos():
    return (-33 + random(), 18 + random())

con = pool.get_conn()

ids = []

with con.cursor() as c:
    c.execute("select id from users")
    ids = c.fetchall()


print(ids)

for i in ids:
    uid = i["id"]
    lat, lng = pos()
    with con.cursor() as c:
        c.execute("""UPDATE users set latitude=%s, longitude=%s where id=%s""", (lat, lng, uid))


pool.release(con)



