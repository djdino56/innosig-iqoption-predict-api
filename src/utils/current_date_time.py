import datetime
import time
import pytz
import dateparser


def add_timestamps(_fields: dict, is_update: bool) -> dict:
    if not is_update:
        _fields['_created'] = get_current_datetime()
    _fields['_updated'] = get_current_datetime()
    return _fields


def get_current_datetime() -> datetime:
    """
    Return the current date_time with the given timezone.
    :return: peewee DateTime object
    """
    return datetime.datetime.now(pytz.timezone('Europe/Amsterdam'))


def get_future_datetime(seconds: int) -> datetime:
    return datetime.datetime.now(pytz.timezone('Europe/Amsterdam')) + datetime.timedelta(seconds=seconds)


def get_past_datetime_by_day(days: int) -> datetime:
    return datetime.datetime.now(pytz.timezone('Europe/Amsterdam')) - datetime.timedelta(days=days)


def is_timeframe_passed(date_time: datetime, seconds: int):
    _old_timestamp = date_time.timestamp()
    _future_datetime = _old_timestamp + seconds
    _timestamp_now = datetime.datetime.now().timestamp()
    return _future_datetime < _timestamp_now


def readable_date_time_string(epoch: float) -> str:
    return datetime.datetime.fromtimestamp(epoch).strftime('%c')


def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds
    :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str
    :return:
         None if unit not one of m, h, d or w
         None if string not in correct format
         int value of interval in milliseconds
    """
    ms = None
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    return ms


def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def seconds_left(timestamp, interval):
    seconds = 60
    if interval == "1m":
        seconds = 60
    elif interval == "5m":
        seconds = 300
    elif interval == "1h":
        seconds = 3600
    elif interval == "4h":
        seconds = 14400
    elif interval == "1d":
        seconds = 24 * 3600
    else:
        print("Interval error!")
        quit()
    current_time = time.time()
    needed_timestamp = timestamp + seconds
    return needed_timestamp - current_time
