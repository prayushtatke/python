from datetime import datetime
from os import getenv
from common_utils.utils.commons import is_not_empty, get_logger
from json import dumps

ENABLE_ALERTS_HANDLING = getenv('ENABLE_ALERTS_HANDLING', False)

class AlertsHandler:
    """
    Usage:
    from utils.alerts import AlertsHandler

    ah = AlertsHandler(stream_name=<name>, stream_client=<Firehose Client>)

    ah.handle(err_code=<code>, err_msg=<msg>, exception=<>, kwarg1=val1, kwarg2=val2)
    """

    logger = get_logger('AlertsHandler')

    def __init__(self,stream_name=None, stream_client=None):

        assert is_not_empty(stream_name), \
            "Firehose delivery stream name cannot be empty."

        assert is_not_empty(stream_client), \
            "Stream Client not provided."

        self.stream_name = stream_name
        self.stream_client = stream_client


    def handle(self, err_code=None, err_msg=None, exception=None, **kwargs ):
        """
        This function takes either (err_code,err_msg) or exception as argument
        It creates a payload in the form of dict:
        { 'err_code' :  <>,
          'err_msg' : <>,
          'err_ts': <>,
          // appends other named arguments.
        }
        this way application can handle what fields are required to be part of payload.

        A json string is created out of this payload and sent to firehose.

        Note: if ENABLE_ALERTS_HANDLING is false, the function call will be no-op.
        :param err_code:
        :param err_msg:
        :param exception:
        :param kwargs:
        :return:
        """
        if not ENABLE_ALERTS_HANDLING:
            return

        if exception:
            self.__handle_excptn(exception, **kwargs)

        elif err_code and err_msg:
            self.__handle_err(err_code, err_msg, **kwargs)


    def __handle_err(self, err_code, err_msg, **kwargs):
        if not ENABLE_ALERTS_HANDLING:
            return

        assert is_not_empty(err_code) and is_not_empty(err_msg), \
            "'err_code', 'err_msg' can not be empty."

        alert_payload = self.create_alert_payload(err_code, err_msg, **kwargs)
        alert_payload_str = dumps(alert_payload) + '\n'
        self.stream_client.write_record(stream_name=self.stream_name, record=alert_payload_str.encode())


    def __handle_excptn(self, exception, **kwargs):
        excptn_name =  type(exception).__name__
        if excptn_name in ['InvalidInputException', 'UDMException', 'UnknownAppException']:
            return self.__handle_err(err_code=exception.err_code.value, err_msg=exception.err_msg, **kwargs)
        else:
            return self.__handle_err(err_code=excptn_name, err_msg=str(exception), **kwargs)

    @classmethod
    def create_alert_payload(cls, err_code, err_msg, **kwargs):
        utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        alert_payload = {
            'err_code': err_code,
            'err_msg': err_msg,
            'err_ts': utc_time
        }

        alert_payload.update(kwargs)
        return alert_payload



