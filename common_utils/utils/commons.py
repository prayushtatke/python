import logging
from contextlib import suppress


# Get Logger Function
def get_logger(logger_name, log_level='DEBUG', log_format='%(asctime)s:%(levelname)s: %(message)s'):
    """
    Returns a logger
    :param logger_name:
    :param log_level:
    :param log_format:
    :return:
    """
    log_level = logging.getLevelName(log_level)
    logging.getLevelName(log_level)
    logging.basicConfig(format=log_format, level=log_level)
    log = logging.getLogger(logger_name)
    log.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter(log_format)
    ch.setFormatter(formatter)

    return log


util_logger = get_logger(__name__)


# ------- Decorators -------- #
def log_exception(logger=None, err_msg='', catch=Exception):
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
            log = logger if logger else util_logger
            try:
                response = func(*args, **kwargs)
                return response
            except catch as e:
                # this is to capture the raised exception message
                log.error(str(e))
                log.exception(err_msg)


        return wrapper


    return inner


def raise_exception(logger=None, err_msg='', catch=Exception, throw=None):
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
            log = logger if logger else util_logger

            try:
                return func(*args, **kwargs)
            except catch as e:
                # this is to capture the raised exception message
                log.error(str(e))
                msg = err_msg if err_msg else str(e)
                if throw:
                    raise throw(msg)
                else:
                    raise


        return wrapper


    return inner


# General Purpose Functions

def is_not_empty(var):
    """
    This is utility method, takes parameter of any type.
    check the exitence of a value.
    e.g. Tests:
        self.assertFalse(util.is_not_empty(None))
        self.assertFalse(util.is_not_empty(''))
        self.assertFalse(util.is_not_empty(' '))
        self.assertFalse(util.is_not_empty({}))
        self.assertFalse(util.is_not_empty([]))

        self.assertTrue(util.is_not_empty(False))
        self.assertTrue(util.is_not_empty(' A '))
        self.assertTrue(util.is_not_empty([1]))
        self.assertTrue(util.is_not_empty({"key" : None}))
        self.assertTrue(util.is_not_empty(1))
        self.assertTrue(util.is_not_empty(1.000))
        self.assertTrue(util.is_not_empty(0))
        self.assertTrue(util.is_not_empty(0.0))
    :param var:
    :return: bool
    """
    if var is None:
        return False

    if var == 0 or False:
        return True

    if var:
        return True if str(var).strip() else False

    return False


def is_empty(var):
    """
        This is utility method, takes parameter of any type.
        check the NON exitence of a value.
        e.g. Tests:
        self.assertTrue(util.is_empty(None))
        self.assertTrue(util.is_empty(''))
        self.assertTrue(util.is_empty('    '))
        self.assertTrue(util.is_empty({}))
        self.assertTrue(util.is_empty([]))

        self.assertFalse(util.is_empty(False))
        self.assertFalse(util.is_empty(' A '))
        self.assertFalse(util.is_empty([1]))
        self.assertFalse(util.is_empty({"key" : None}))
        self.assertFalse(util.is_empty(1))
        self.assertFalse(util.is_empty(1.000))
        self.assertFalse(util.is_empty(0))
        self.assertFalse(util.is_empty(0.0))

        :param var:
        :return: bool
    """
    return not is_not_empty(var)


def find_missing_or_empty_keys(input_coll, key_set):
    """
        Returns the list of missing keys in input collection.
        This is particularly helpful when we have to check multiple
        keys in a collection. it can simplifies the if condition.

        e.g. Usage.

        missing_keys = find_missing_or_empty_keys(payload, [C_NAME, C_ASSET_ID, AGG_WINDOW, SIGNALS])
        if missing_keys:
            log.error(
                f'Missing required fields[{str(missing_keys)}] in the input, input_payload: {str(payload)}')
            raise MissingRequiredInput(f'Missing Required fields[{str(missing_keys)}].')

    :param input_coll:
    :param key_set: keys to search
    :return:
    """
    if (not input_coll) or (not key_set):
        return None

    return list(filter(lambda e: e not in input_coll or is_empty(input_coll[e]), key_set))


def del_dict_keys(input_dict, keys_to_del):
    assert is_not_empty(input_dict) and isinstance(input_dict, dict), \
        "'input_dict' cannot be empty, and should be type of 'dict'"

    with suppress(KeyError):
        for k in keys_to_del:
            del input_dict[k]


def retry(exceptions=Exception, tries=4, delay=3, backoff=0, logger=None):
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
            log = logger if logger else util_logger
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return func(*args, **kwargs)
                # Retry only for provided exception
                except exceptions as e:
                    msg = f'{str(e)}, Retrying in {mdelay} seconds...'
                    log.error(str(e))
                    log.error(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay = mdelay + delay if backoff else delay
            return func(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry