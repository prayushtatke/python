import json
from base64 import b64decode
from os import getenv
from src.status.status import StatusFactory
from common_utils.utils.commons import get_logger, is_empty

class KinesisLambdaHandler:
    def __init__(self, status_impl, conf, mock_client_redis=None):
        self.impl = status_impl(conf, mock_client_redis)

    def __decode(self, kinesis_record):
        """
        :param kinesis_record: raw record from kinesis.
        :return: dict
        """
        try:
            in_payload = b64decode(kinesis_record['kinesis']['data'])
            return json.loads(in_payload, encoding='utf-8')
        except Exception as e:
            log.exception(f'Error decoding kinesis record: {str(kinesis_record)}')
        return None

    def handle_event(self, kinesis_event):
        input_iter = map(lambda rec: self.__decode(rec), kinesis_event['Records'])
        for payload in input_iter:
            self.impl.enrich_payload(payload)


log = get_logger(__name__, log_level=LOG_LEVEL, log_format=LOG_FORMAT)
is_init = False
lambdaHandler = None


def validate_env_vars(required_env_vars):
    """
    required_env_vars: list of mandatory env variable keys
    """
    missing_envs = [env for env in required_env_vars if is_empty(getenv(env))]
    if missing_envs:
        raise KeyError(f'Missing environ variables: {str(missing_envs)}')


def init():
    global is_init, lambdaHandler
    if is_init:
        return

    try:
        validate_env_vars(['ENV_VAR_1', 'ENV_VAR2'])
        impl = StatusFactory.get_status_impl(C_NAMES)
        config = {}
        lambdaHandler = KinesisLambdaHandler(impl, config)
        log.debug('Lambda Intitialized Successfully')
        is_init = True
    except Exception as e:
        log.exception(f'Lambda initialization failed. {str(e)}')
    return is_init


def handler(event, context):
    if not is_init:
        # invoke init
        if not init():
            raise Exception('Lambda Initialization Failed.')
    try:
        lambdaHandler.handle_event(event)
    except Exception as e:
        log.error(f'Event Handling Failed: {str(e)}')
        raise e
