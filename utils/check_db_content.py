from db_connector import db_connector
import configparser
import os
# TODO add logging config and configure logs for the whole project
# TODO for file and console
import logging
import datetime
from utils import misc
from psycopg2 import sql
from news import news3k


prj_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
cfg_path = os.path.join(prj_root, 'config/db.ini')

db_config = misc.read_if_exists(cfg_path)


dc = db_connector.DBConnector(
    password=db_config['DB_CONFIG']['db_pwd'],
    user=db_config['DB_CONFIG']['db_user'],
    db=db_config['DB_CONFIG']['db_name'],
    host="172.17.0.2",
    port=5432
)

conn = dc.connect()
rs = dc._exec_query(f"SELECT * FROM ru_news")
for j in rs:
    print(j)
# for t in "ru_news":
#         #, 'us_news', 'ge_news':
#     logging.info(f'Table -> {t}')
#     rs = dc._exec_query(f'SELECT * FROM {t}')
