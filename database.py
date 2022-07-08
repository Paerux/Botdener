import json
from contextlib import contextmanager
from datetime import datetime

DATABASE_FILE = 'uyanmis.json'
DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"


@contextmanager
def access_database():
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = dict()

    yield data

    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def add_uyanmis(id, time):
    with access_database() as data:
        data[id] = time

def get_last_uyanmis(id):
    with access_database() as data:
        try:
            date = data[id]
            return datetime.strptime(date, DATE_FORMAT)
        except KeyError as e:
            print(e)
