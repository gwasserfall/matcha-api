import config
import threading
from database_pool import Pool

from time import sleep

pool = Pool(max_size=10, **config.database)

def count_connection():
    while True:
        print("Active connections = ", pool.get_pool_size())
        sleep(3)


t = threading.Thread(target=count_connection, daemon=True)

t.start()