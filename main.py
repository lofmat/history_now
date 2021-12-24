#!/usr/bin/env python3

from db_connector import db_connector
from datetime import datetime
import json
import multiprocessing as mp
import os
import logging
#from schema import Schema, And, Use


from utils import misc
from psycopg2 import sql
from news import news3k

root_dirname = os.path.abspath(os.path.dirname(__file__))
cfg_path = os.path.join(root_dirname, 'config/db.ini')
src_cfg_path = os.path.join(root_dirname, 'config/sources.ini')

# ;news_date = DATE
# ;news_tag = VARCHAR(164)
# ;news_author = VARCHAR(164)
# ;news_title = VARCHAR(164)
# ;news_source = VARCHAR(164)
# ;news_text = TEXT
# news_schema = Schema(['news_date': And(Use(float), lambda n: 0.0 <= n <= 100.0),
#                               'news_tag': Use(str),
#                               'news_author': And(Use(int), lambda n: 0 <= n),
#                               'news_title': And(Use(int), lambda n: 0 <= n)
#                        'news_source':,
#                        'news_text'
#                     ])
#


now = datetime.now() # current date and time
time_stamp = now.strftime("%m%d%Y-%H%M%S")


logging.basicConfig(level=logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

log_path = os.path.join(root_dirname, 'logs', f'{time_stamp}-processing.log')

fileHandler = logging.FileHandler(log_path, mode='a')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

db_config = misc.read_if_exists(cfg_path)
sources_config = misc.read_if_exists(src_cfg_path)
dc = db_connector.DBConnector(
    password=db_config['DB_CONFIG']['db_pwd'],
    user=db_config['DB_CONFIG']['db_user'],
    db=db_config['DB_CONFIG']['db_name'],
    host=db_config['DB_CONFIG']['db_host'],
    port=db_config['DB_CONFIG']['db_port']
)
conn = dc.connect()


def store_data(newspaper_link: str) -> None:
    dt = news3k.get_np3k_data(newspaper_link.strip())
    if len(dt):
        logging.info('Fetched data > 0')
    else:
        logging.error('No data fetched')
    for row in dt:

        dc.insert(table=sources_config[r]['table_name'],
                  columns=['news_date', 'news_tag', 'news_author', 'news_title', 'news_source', 'news_text'],
                  values=list(row))


# TODO in case if docker is down write the data to CSV
dc._exec_query("SET datestyle = dmy")

for r in sources_config.sections():
    logging.info(f'Current location is -> {r}')
    # (art.publish_date, art.meta_keywords, art.authors, art.title, art.text)
    logging.info('Creating table if not exist.')
    # TODO get columns, values from config
    q_create_table = sql.SQL("CREATE TABLE IF NOT EXISTS {table} "
                             "(news_date DATE, "
                             "news_tag VARCHAR(1024), "
                             "news_author VARCHAR(1024), "
                             "news_title VARCHAR(1024), "
                             "news_source VARCHAR(1024), "
                             "news_text TEXT)").format(table=sql.Identifier(sources_config[r]['table_name']))
    dc._exec_query(q_create_table)
    #
    # results = pool.map(howmany_within_range_rowonly, [row for row in data])
    # results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]
    #
    # pool.close()
    pool = mp.Pool(mp.cpu_count())
    print(sources_config.get(r, 'news'))
    n_links = json.loads(sources_config.get(r, 'news'))
    # TODO hack, fix it. Lists in INI config
    logging.info(f'Current resources -> {n_links}')
    pool.map(store_data, n_links)
    pool.close()

#dc._exec_query("CREATE TABLE IF NOT EXISTS {t} (news_date DATE, news_source VARCHAR(164), news_tag VARCHAR(164), news_author VARCHAR(164), news_text TEXT)".format(t=sql.Identifier(r)))
#for url in
#news3k.get_np3k_data()
# dc.insert(table='history_20_07_77', columns=['news_date','news_source', 'news_tag', 'news_author', 'news_text'], values=[datetime.datetime(2020, 12, 17), 'https://www.site1.ru', 'Aith', 'sport', 'some text blablabla'])
# dc.insert(table='history_20_07_77', columns=['news_date','news_source', 'news_tag', 'news_author', 'news_text'], values=[datetime.datetime(2020, 12, 13), 'https://www.site123.ru','sport', 'Uskj tkl', 'some text blablabla fffdd'])
# dc.insert(table='history_20_07_77', columns=['news_date','news_source', 'news_tag', 'news_author', 'news_text'], values=[datetime.datetime(2020, 12, 11), 'https://www.site144.ru', 'sport', 'Jxxx Xjk', 'some text blablabla fffdd 1111'])
# rs = dc._exec_query('SELECT * FROM history_20_07_77')
#print(rs[0][0].strftime("%m-%d-%Y, %H-%M-%S"))
