import logging


class Logger:
    '''
    Default logging class. Does not for use with file handler.
    '''
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

    def __init__(self, name, log_level='DEBUG'):
        '''
        Constructor
        :param name: Class or Function __name__
        :type name: str
        :param log_level: Log level. One of ('INFO', 'DEBUG', 'WARNING', 'ERROR')
        :type log_level: str
        '''
        self.name = name
        self.log_format = '%(asctime)s - %(levelname)s - %(name)s: %(message)s'
        self.log_level = self.__get_log_level(log_level)
        self.logger = self.__get_logger()

    def __get_log_level(self, level):
        switcher = {
            'DEBUG'  :logging.DEBUG,
            'INFO'   :logging.INFO,
            'WARNING':logging.WARNING,
            'ERROR'  :logging.ERROR
        }
        return switcher.get(level, lambda:logging.DEBUG)

    def __get_logger(self):
        logger = logging.getLogger(self.name)
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter(self.log_format)
        c_handler.setFormatter(c_format)
        if not logger.handlers:
            logger.addHandler(c_handler)
        logger.setLevel(self.log_level)
        return logger

    def set_log_level(self, log_level):
        '''
        Set log level.
        :param log_level: Log level. One of ('INFO', 'DEBUG', 'WARNING', 'ERROR')
        :type log_level:
        :raises: TypeError for invalid log_level
        '''
        if log_level not in (self.INFO, self.DEBUG, self.WARNING, self.ERROR):
            raise TypeError(f'Invalid log level {log_level}')
        self.log_level = log_level
        self.logger = self.__get_logger()

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)
