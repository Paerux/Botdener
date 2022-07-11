import json
from contextlib import contextmanager
from datetime import datetime

DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"


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
    with access_database('uyanmis.json') as data:
        data[userid] = time


def get_last_uyanmis(userid):
    with access_database('uyanmis.json') as data:
        try:
            date = data[userid]
            return datetime.strptime(date, DATE_FORMAT)
        except KeyError as e:
            print(e)


def get_rss_list():
    with access_database('rssdb.json') as data:
        try:
            return data
        except KeyError as e:
            print(e)


def add_rss_id(guid):
    with access_database('rssdb.json') as data:
        data[guid] = 'seen'
