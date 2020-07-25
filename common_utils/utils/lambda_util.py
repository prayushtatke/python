import common_utils.utils.commons as util
from ast import literal_eval
import common_utils.utils.aws as aws
from common_utils.utils.logger import Logger

class Lambda(aws.Client):
    client_type = 'lambda'
    logger = Logger('Lambda')


    def check_lambda_exist(self, lambda_name):
        assert util.is_not_empty(lambda_name), \
            "lamdba name cannot be empty."

        l_client = self.get_or_create_client()
        exist = False
        try:
            resp = l_client.get_function(FunctionName=lambda_name)
            return resp is not None
        except Exception as e:
            self.logger.exception(str(e))

        return exist


    def invoke(self, name, payload, invocation_type='RequestResponse'):
        """
        Invokes a given lambda
        :param name: name of the lambda function
        :param payload: lambda event
        :param invocation_type: default requestresponse
        :return: response
        """
        assert util.is_not_empty(name), \
            "Lambda Name cannot be empty."

        assert util.is_not_empty(payload), \
            "Lambda Payload cannot be empty."

        l_client = self.get_or_create_client()

        response = l_client.invoke(
            FunctionName=name,
            InvocationType=invocation_type,
            Payload=payload
        )
        if invocation_type == 'Event':
            return

        payload_str = response['Payload'].read().decode('utf-8')
        payload = literal_eval(payload_str)
        return payload