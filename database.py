import config
from helpers.pymysqlpool import Pool

from threading import Thread
from time import sleep

pool = Pool(max_size=10, timeout=2, **config.database)
