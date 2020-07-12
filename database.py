import config
import threading
from helpers.pymysqlpool import Pool

from time import sleep

pool = Pool(max_size=10, **config.database)

def count_connection():
    while True:
        # if pool.is_active:
        #     connection = pool.get_conn()
        #     with connection.cursor() as c:
        #         c.execute("show status where `variable_name` = 'Threads_connected';")
        #         print(c.fetchone())
        #     pool.release(connection)
        print("Active connections = ", pool.get_pool_size())
        sleep(3)


t = threading.Thread(target=count_connection, daemon=True)

t.start()