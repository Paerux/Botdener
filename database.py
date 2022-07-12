import json
import logging
from contextlib import contextmanager
from datetime import datetime

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %z"


@contextmanager
def access_database(database_file):
    try:
        with open(database_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = dict()

    yield data

    with open(database_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def add_uyanmis(userid, time):
    with access_database('db/uyanmis.json') as data:
        data[userid] = time


def get_last_uyanmis(userid):
    with access_database('db/uyanmis.json') as data:
        try:
            date = data[userid]
            return datetime.strptime(date, DATE_FORMAT)
        except KeyError as e:
            logging.getLogger(__name__).error(e)


def get_rss_list():
    with access_database('db/rssdb.json') as data:
        try:
            return data
        except KeyError as e:
            logging.getLogger(__name__).error(e)


def add_rss_id(key, date):
    with access_database('db/rssdb.json') as data:
        data[key] = date
