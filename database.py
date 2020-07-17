import config
from helpers.pymysqlpool import Pool

pool = Pool(max_size=10, **config.database)