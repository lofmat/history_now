import logging
from configparser import ConfigParser, ExtendedInterpolation, MissingSectionHeaderError
import os


def read_if_exists(cfg_path):
    r = None
    cp = ConfigParser(interpolation=ExtendedInterpolation())
    if os.path.exists(cfg_path) and os.path.isfile(cfg_path):
        try:
            cp.read(cfg_path)
            r = cp
        except MissingSectionHeaderError as e:
            logging.exception(f"It isn't INI config -> {cfg_path}. Exception -> {e}")
    else:
        logging.error(f"No such config -> {cfg_path}")
    return r
#
# print(read_if_exists('/home/isuntcov/PycharmProjects/history_now/config/sources.ini'))
# r = read_if_exists('/home/isuntcov/PycharmProjects/history_now/config')
# print(r)
# print(read_if_exists('/home/isuntcov/PycharmProjects/history_now/config/source1.ini'))
# print(read_if_exists('/home/isuntcov/PycharmProjects/history_now/db_connector/db_connector.py'))
#
