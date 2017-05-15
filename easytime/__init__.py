#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union, Optional

import time
import datetime
import pytz
from dateutil.tz import tzlocal


utc = pytz.utc
local = tzlocal()


def tz(name: str) -> datetime.tzinfo:
    """Returns a tzinfo object with the given name."""
    if name == 'utc':
        return pytz.utc
    elif name == 'local':
        return tzlocal()
    else:
        return pytz.timezone(name)


def ts(year: int, month: int, day: int,
       hour: int=0, minute: int=0, second: int=0,
       microsecond: int=0) -> float:
    """
    >>> ts(year=1970, month=1, day=1)
    0.0

    >>> ts(year=2011, month=5, day=31, hour=19, minute=0, second=1)
    1306868401.0
    """
    t0 = time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))
    t1 = time.mktime((year, month, day, hour,
                      minute, second, microsecond,
                      0, 0))
    return t1 - t0


def dt(days: float=0, hours: float=0, minutes: float=0, seconds: float=0,
       miliseconds: float=0, microseconds: float=0) -> float:
    """
    >>> dt(days=2, hours=1, minutes=30, seconds=12, miliseconds=32,
    ...    microseconds=123)
    178212.032123

    >>> dt(minutes=2, seconds=66) == 2 * 60 + 66
    True
    """
    hours += days * 24
    minutes += hours * 60
    seconds += minutes * 60

    microseconds += miliseconds * 1000
    seconds += microseconds / 1e6

    return seconds


def now() -> float:
    """
    >>> now() # doctest: +SKIP
    1425131462.31405
    """
    return time.time()


def strptime(text: str, format: str, timezone: datetime.tzinfo) -> float:
    if isinstance(timezone, str):
        timezone = tz(timezone)
    elif not isinstance(timezone, datetime.tzinfo):
        raise ValueError("Unknown timezone.")

    dt = datetime.datetime.strptime(text, format)
    return datetime_to_timestamp(dt, timezone)


def strftime(timestamp: float, format: str, timezone: datetime.tzinfo) -> str:
    if isinstance(timezone, str):
        timezone = tz(timezone)
    elif not isinstance(timezone, datetime.tzinfo):
        raise ValueError("Unknown timezone.")

    dt = timestamp_to_datetime(timestamp, timezone)
    return dt.strftime(format)


def datetime_to_timestamp(dt: datetime.datetime,
                          timezone: Optional[datetime.tzinfo]=None
                          ) -> float:
    """Converts a datetime object to UTC timestamp"""

    if dt.tzinfo is None:
        if isinstance(timezone, str):
            timezone = tz(timezone)
        dt = dt.replace(tzinfo=timezone)

    t0 = time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))
    t1 = time.mktime(dt.utctimetuple())
    return t1 - t0


def timestamp_to_datetime(ts: float,
                          tz_str: Union[str, datetime.tzinfo]
                          ) -> datetime.datetime:
    if isinstance(tz_str, str):
        timezone = tz(tz_str)

    # FIXME[alex]: pytz is NOT compatible with datetime AFAIU.
    return datetime.datetime.fromtimestamp(ts, timezone) # type: ignore


def now_datetime(tz_str: Union[str, datetime.tzinfo]) -> datetime.datetime:
    if isinstance(tz_str, str):
        timezone = tz(tz_str)
    else:
        timezone = tz_str

    return datetime.datetime.now(timezone)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
