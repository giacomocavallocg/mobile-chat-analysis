from enum import Enum
from datetime import datetime


def read_file(path):
    with open(path, encoding="utf8") as f:
        return f.read()


def parse_datetime(date, time):
    dt = datetime.strptime(" ".join((date, time)), '%d/%m/%y %H:%M')
    # dt = datetime.strptime(" ".join((date, time)), '%d/%m/%y %H:%M:%S')
    day = dt.strftime("%a")
    return dt, day


class Lang(Enum):
    IT = 1
    EN = 2


class Source(Enum):
    IOS = 1,
    ANDROID = 2,
