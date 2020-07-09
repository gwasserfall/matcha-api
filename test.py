
from config import database

# from pymysqlpool.pool import Pool
from threading import Thread, Timer
import threading



from database_pool import Pool



pool = Pool(ping_check=10, max_size=10, **database)
pool.init()

def query(name):

    con = pool.get_conn()

    with con.cursor() as c:
        c.execute("Select %s as ThreadNumber", (name))
        print(c.fetchone(), "Pool size =", pool.get_pool_size())

    pool.release(con)


query(1)
pool.destroy()
