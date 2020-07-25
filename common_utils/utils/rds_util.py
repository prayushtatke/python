import pg8000
from common_utils.utils import commons as util
from common_utils.utils.configstore import ConfigStore
from common_utils.utils.decorators import return_opt_empty_when_error
from common_utils.utils.optional import Optional

from common_utils.utils.logger import Logger


class RDSException(Exception):
    pass


class RDS:


    @classmethod
    def get_client(cls, rds_db=None, rds_port=None, rds_username=None, rds_password=None, rds_host=None):
        """
         Returns new Redis client.
         @param rds_db:
         @param rds_port:
         @param rds_username:
         @param rds_password:
         @param rds_host:
         @return:

        """
        return pg8000.connect(database=rds_db, port=rds_port, user=rds_username, password=rds_password, host=rds_host)

    def __init__(self, db=None, port=5432, username=None, password=None, host=None,
                 aws_secret_name=None, aws_param_name=None,
                 aws_region='eu-west-1', secured_param=False, test_client=None,log_level="INFO"):
        """
        @param db:
        @param port:
        @param username:
        @param password:
        @param host:
        @param aws_secret_name:
        @param aws_param_name:
        @param aws_region:
        @param secured_param:
        @param test_client:


        """
        self.logger = Logger(__name__,log_level)
        self.logger.info('Connecting to Rds Database')
        self.username, self.host, self.port, self.password = None, None, None, None
        if all([host, port, password, username]):
            self.host, self.port, self.password, self.username = host, port, password, username

        # get configs from aws parameter store
        elif aws_param_name is not None:
            params = ConfigStore.get_config(aws_param_name, store_type='params', secured=secured_param)
            self.__validate_params(params, ['username', 'password', 'hostname'])
            prt = int(params.get('port')) if params.get('port') else port
            database = params.get('db_name') if params.get('db_name') else db
            self.host, self.port, self.password, self.username, self.db = params['hostname'], prt, params['password'], \
                                                                          params['username'], database

        # used for unit testing
        elif test_client is not None:
            self.connection = test_client

        try:
            if not test_client:
                self.connection = RDS.get_client(self.db, self.port, self.username, self.password, self.host)
            self.logger.info('Connection to rds database established')
        except Exception as e:
            self.logger.error(str(e))
            raise RDSException(str(e))

    def __validate_params(self, params, keys):
        missing_keys = util.find_missing_or_empty_keys(params, keys)
        if missing_keys:
            self.logger.error(f'Missing required Params[{str(missing_keys)}] in Secret/Param store')
            raise RDSException(f'Missing Required fields[{str(missing_keys)}].')

    @return_opt_empty_when_error()
    def fetch_data(self, query):

        with self.connection.cursor() as cur:
            self.logger.debug('Query Execution Started !!!')
            cur.execute(query)
            cols = [a[0].decode("utf-8") for a in cur.description]
            self.logger.debug('RDS Meta Data Column Names: %s' % cols)
            records = [{a: b for a, b in zip(cols, row)} for row in cur.fetchall()]

            opt_val = Optional(records)

            if not opt_val.is_present():
                return Optional.empty()
            return opt_val
