import time
from datetime import datetime, timedelta, timezone
from enum import Enum


# TimeUnit = Enum('TimeUnit', ['MILL', 'SECS', 'MINS', 'HRS', 'DAYS', 'WKS', 'MTHS', 'YRS'])
class TimeUnit(Enum):
    SECS = 'secs'
    MINS = 'mins'
    HRS = 'hr'
    DAYS = 'days'
    WKS = 'wks'
    MTHS = 'months'
    YR = 'yr'


py_tz = None


def get_tzinfo(offset: str = None, tz: str = None):
    global py_tz
    if offset:
        if ":" in offset:
            hour, minutes = map(lambda i: int(i), offset.split(":"))
        else:
            hour, minutes = int(offset[:-2]), int(offset[-2:])
        if hour >= 0:
            tzinfo = timezone(timedelta(hours=abs(hour), minutes=minutes))
        else:
            tzinfo = timezone(-timedelta(hours=abs(hour), minutes=minutes))
    elif tz:
        if not py_tz:
            from pytz import timezone as py_tz
        tzinfo = py_tz(tz)
    else:
        tzinfo = timezone.utc
    return tzinfo


def to_datetime(ts_str: str, fmt: str = "%Y-%m-%d %H:%M:%S",
                tz_in: str = None, tz_out: str = None,
                in_tz_offset: str = None, out_tz_offset: str = None) -> datetime:
    if (not ts_str) or (not fmt):
        return None

    intz = get_tzinfo(in_tz_offset, tz_in)
    outtz = get_tzinfo(out_tz_offset, tz_out)

    return datetime.strptime(ts_str, fmt) \
        .replace(tzinfo=intz) \
        .astimezone(tz=outtz)


def datetime_tostr(dt: datetime = datetime.now(), fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    if (not dt) or (not fmt):
        return None

    return dt.strftime(fmt)


def timeit(method):
    """
    Decorator to time functions.
    """

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%s  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def utc_now() -> int:
    return int(datetime.utcnow().timestamp())


def to_epoch(ts_str: str, fmt: str = '%Y-%m-%d %H:%M:%S', tz_in: str = None, tz_out: str = None,
             ofst_in: str = None, ofst_out: str = None) -> int:
    return int(to_datetime(ts_str, fmt, tz_in, tz_out, ofst_in, ofst_out).replace(tzinfo=timezone.utc).timestamp())


def to_epoch_ms(ts_str: str, fmt: str = '%Y-%m-%d %H:%M:%S', tz_in: str = None, tz_out: str = None,
             ofst_in: str = None, ofst_out: str = None) -> int:
    return int(to_datetime(ts_str, fmt, tz_in, tz_out, ofst_in, ofst_out).replace(tzinfo=timezone.utc).timestamp() * 1000)


def utc_now_str() -> str:
    return datetime_tostr(datetime.utcnow())


def utc_time_delta(seconds=0, minutes=0,
                   hours=0, days=0, weeks=0, utc_dt=datetime.utcnow()):
    return time_delta(seconds, minutes, hours, days, weeks, utc_dt)


def utc_time_delta_epoch(seconds=0, minutes=0,
                         hours=0, days=0, weeks=0, epoch: int = None, utc_dt=datetime.utcnow()):
    dtime = datetime.fromtimestamp(epoch, timezone.utc) if epoch else utc_dt
    return int(time_delta(seconds, minutes, hours, days, weeks, dtime).timestamp())


def time_delta(seconds=0, minutes=0,
               hours=0, days=0, weeks=0, dt=datetime.now()) -> datetime:
    td = None
    if seconds:
        td = timedelta(seconds)
    elif minutes:
        td = timedelta(minutes)
    elif hours:
        td = timedelta(hours)
    elif days:
        td = timedelta(days)
    elif weeks:
        td = timedelta(weeks)

    return dt - td


def time_delta_epoch(seconds=0, minutes=0,
                     hours=0, days=0, weeks=0, epoch: int = None, dt: datetime = datetime.now()) -> int:
    dtime = datetime.fromtimestamp(epoch) if epoch else dt
    return int(time_delta(seconds, minutes, hours, days, weeks, dtime).timestamp())


def is_ts_diff_limit_exceeded(ts1, ts2, limit, unit: TimeUnit = TimeUnit.SECS, fmt='%Y-%m-%d %H:%M:%S'):
    """
        Note: ts1 and ts2 should be in same timezone
    """
    if type(ts1) != type(ts2):
        raise TypeError('Both timestamp should be of same type.')

    ts1_secs, ts2_secs = ts1, ts2
    if isinstance(ts1, datetime) and isinstance(ts2, datetime):
        ts1_secs = int(ts1.timestamp())
        ts2_secs = int(ts2.timestamp())

    if isinstance(ts1, str) and isinstance(ts2, str):
        ts1_secs = to_epoch(ts1, fmt)
        ts2_secs = to_epoch(ts2, fmt)

    lmt_secs = limit
    if unit == TimeUnit.MINS:
        lmt_secs = limit * 60
    elif unit == TimeUnit.HRS:
        lmt_secs = limit * 60 * 60
    elif unit == TimeUnit.DAYS:
        lmt_secs = limit * 24 * 60 * 60

    # TODO: Note: below is only for completeness. Have to be tested before use.
    elif unit == TimeUnit.WKS:
        lmt_secs = limit * 7 * 24 * 60 * 60
    elif unit == TimeUnit.MTHS:
        lmt_secs = limit * 30 * 24 * 60 * 60
    elif unit == TimeUnit.YR:
        lmt_secs = limit * 365 * 24 * 60 * 60

    return int(ts1_secs - ts2_secs) >= lmt_secs
