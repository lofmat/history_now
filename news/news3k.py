import datetime

import newspaper
from newspaper.article import ArticleException
from newspaper import Config
import logging
from newspaper import Article
# url = 'https://www.berliner-zeitung.de/'
# url_meduza  = "https://meduza.io/"
cfg = Config()
cfg.request_timeout = 15

logging.basicConfig(level=logging.INFO)
# SEP = '#'
# sep_line = SEP * 30

# class NewspaperData:
#     def __init__(self, source):
#         self.source = source


def get_np3k_data(url: str) -> list:
    # list of tuples
    rs = []
    data = newspaper.build(url, memoize_articles=False, config=cfg)
    for art in data.articles:
        try:
            art.download()
            art.parse()
            # Sometimes publish date is empty
            rs.append((art.publish_date if art.publish_date else datetime.datetime.now(),
                       art.meta_keywords,
                       art.authors,
                       art.title,
                       url, art.text))
        except ArticleException as e:
            logging.exception(f'Exception -> {e}')
            logging.exception(f"Cannot download url content -> {url}")
            continue
    return rs
#
# for art in x.articles:
#     logging.info(sep_line)
#     logging.info(f'URL -> {art.url}')
#     try:
#         art.download()
#         art.parse()
#     except ArticleException:
#         logging.info('00000000000000000000000000000000 ')
#         logging.exception(f"Cannot download url content -> {url}")
#         continue
#
#