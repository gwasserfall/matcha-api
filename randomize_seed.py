from database import pool
from random import random, randint



def pos():
    lat_main = -33
    long_main = 18

    lat = lat_main + random()
    lng = long_main + random()
    return (lat, lng)

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



