import common_utils.utils.commons as util


@util.raise_exception(err_msg='Method: get_aws_client(): Error initializing AWS Client.')
def get_aws_client(service_name,
                   region_name=None,
                   aws_access_key_id=None,
                   aws_secret_access_key=None,
                   aws_session_token=None,
                   endpoint_url=None,
                   config=None):
    """
    Utility method to get aws (boto3) client instance.
    :param config:
    :param aws_session_token:
    :param endpoint_url:
    :param aws_secret_access_key:
    :param aws_access_key_id:
    :param region_name:
    :param service_name:
    :param region:
    :return: client
    """
    assert util.is_not_empty(region_name), \
        "AWS Region cannot be empty."

    assert util.is_not_empty(service_name), \
        "client_type cannot be empty."

    from boto3 import client as boto3_client

    return boto3_client(service_name,
                        region_name=region_name,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token,
                        endpoint_url=endpoint_url,
                        config=config)


class Client:
    logger = util.get_logger('AwsUtil')
    client_type = ''

    def __init__(self, region=None, assume_role_arn=None,
                 assume_role_session_name=None, assume_role_duration_sec=None,
                 aws_access_key_id=None, aws_secret_access_key=None,
                 aws_session_token=None, endpoint_url=None,
                 config=None):
        self.client = None
        self.region = region
        self.assume_role_arn = assume_role_arn
        self.assume_role_session_name = assume_role_session_name
        self.assume_role_duration_sec = assume_role_duration_sec
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        self.endpoint_url = endpoint_url
        self.config = config

    def __check_access_params(self):

        if not all((self.assume_role_arn, self.assume_role_session_name,self.assume_role_duration_sec)):
            return

        sts_client = get_aws_client('sts', self.region)
        sts_response = sts_client.assume_role(
            RoleArn=self.assume_role_arn,
            RoleSessionName=self.assume_role_session_name,
            DurationSeconds=int(self.assume_role_duration_sec))

        self.aws_access_key_id = sts_response['Credentials']['AccessKeyId']
        self.aws_secret_access_key = sts_response['Credentials']['SecretAccessKey']
        self.aws_session_token = sts_response['Credentials']['SessionToken']

    def get_new_client(self):
        return self.get_client(
            region=self.region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
            endpoint_url=self.endpoint_url,
            config=self.config)

    def get_or_create_client(self):

        if self.client:
            return self.client

        self.__check_access_params()
        self.logger.info('Creating New AWS Service Client')
        self.client = self.get_new_client()

        return self.client

    @classmethod
    def get_client(cls,
                   region=None,
                   aws_access_key_id=None,
                   aws_secret_access_key=None,
                   aws_session_token=None,
                   endpoint_url=None,
                   config=None):
        """

        :param config:
        :param aws_session_token:
        :param endpoint_url:
        :param aws_secret_access_key:
        :param aws_access_key_id:
        :param region:
        :return:
        """
        return get_aws_client(cls.client_type,
                              region_name=region,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token,
                              endpoint_url=endpoint_url,
                              config=config)
