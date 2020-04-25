import time
from datetime import datetime
from common_utils.utils.logger import Logger


def to_datetime(ts_str: str, pattern: str) -> datetime:
    if (not ts_str) or (not pattern):
        return None

    return datetime.strptime(ts_str, pattern)


def datetime_tostr(dt: datetime, pattern: str) -> str:
    if (not dt) or (not pattern):
        return None

    return dt.strftime(pattern)


def timeit(method):
    """
    Decorator to time functions.
    """
    LOG = Logger(method.__name__)

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        LOG.debug('%s  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def utc_now() -> int:
    return int(datetime.utcnow().timestamp())


def to_epoch(ts_str: str, pattern: str) -> int:
    return int(to_datetime(ts_str, pattern).timestamp())


def to_epoch_ms(ts_str: str, pattern: str) -> int:
    return int(to_datetime(ts_str, pattern).timestamp() * 1000)

