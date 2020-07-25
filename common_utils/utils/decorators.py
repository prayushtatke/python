from time import sleep
from functools import wraps
from common_utils.utils.logger import Logger
from common_utils.utils.optional import Optional

_logger = Logger(__name__)

def log_exception(logger=_logger, err_msg='', catch=Exception):
    """
    This define a decorator, which catch and logs exception from original function
    e.g.
    # below method :
    def foo(**args, **kwargs):
        try:
            // some code
        except KeyError as e:
            log.error(str(e))
            log.exception('OtherMsg')

    # can be written as:

    @log_exception(logger=<app's logger, catch=KeyError, err_msg='OtherMsg' )
    def foo(**args, **kwargs):
        // some code

    here,defaults values for :
    logger =  utils.commons.util_logger
        catch = Exception, it can be Single Exception as well as tuple e.g.
        catch=(KeyError, TypeError)
        err_msg = 'str(e)'
    """

    def inner(func):
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                return response
            except catch as e:
                if err_msg:
                    logger.error(err_msg)
                logger.error(str(e))

        return wrapper

    return inner


def raise_exception(logger=_logger, err_msg='', catch=Exception, throw=None):
    """
    This defines a decorator, which catches the exception from original function
    log the err_msg and re-raise the same exception.

    e.g.
    # below method :
    def foo(**args, **kwargs):
        try:
        // some code
        except KeyError as e:
            log.error(str(e))
            raise WrapperException('WrapperExceptionMsg')

    # can be written as:
    @raise_exception(logger=<app's logger, catch=KeyError, throw=WrapperException, err_msg='WrapperErrorMsg')
    def foo(**args, **kwargs):
        // some code

    here,defaults values for :
    logger =  utils.commons.util_logger
    catch = Exception, it can be Single Exception as well as tuple e.g.
    catch=(KeyError, TypeError)
    throw = None, if none same exception is thrown
    err_msg = 'str(e)'.

    """

    def inner(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except catch as e:
                # this is to capture the raised exception message
                logger.error(str(e))
                msg = err_msg if err_msg else str(e)
                if throw:
                    raise throw(msg)
                else:
                    raise

        return wrapper

    return inner


def retry(exceptions=Exception, tries=4, delay=3, backoff=0, logger=_logger):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """
    def deco_retry(func):

        @wraps(func)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return func(*args, **kwargs)
                # Retry only for provided exception
                except exceptions as e:
                    msg = f'{str(e)}, Retrying in {mdelay} seconds...'
                    logger.error(msg)
                    sleep(mdelay)
                    mtries -= 1
                    mdelay = mdelay + delay if backoff else delay
            return func(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def return_opt_empty_when_error(logger=_logger, err_msg=''):
    """
    This decorator wraps the called function in try-except block and returns Optional.empty() in case of exception.
    e.g.
    # below method :
    def foo(**args, **kwargs):
        try:
            // some code
        except Exception as e:
            log.error("Error occurred while executing foo()\n"+str(e))

    # can be written as:

    @return_opt_empty_when_error(logger=<app's logger>, err_msg='Error occurred while executing foo()')
    def foo(**args, **kwargs):
        // some code
    """
    def inner(func):
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                return response
            except Exception as e:
                msg = '{}\n{}'.format(err_msg, str(e)) if err_msg else str(e)
                logger.error('{}'.format(msg))
                return Optional.empty()
        return wrapper

    return inner