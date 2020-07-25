import boto3
from botocore.exceptions import ClientError
from common_utils.utils import aws
from common_utils.utils.decorators import raise_exception
from common_utils.utils.logger import Logger

class SQSClient(aws.Client):
    client_type = 'sqs'
    logger = Logger('SQSClient')

    def __init__(self, sqs_url, **kwargs):
        super(SQSClient, self).__init__(**kwargs)
        self.sqs_url = sqs_url

    @raise_exception(catch=ClientError, logger=logger)
    def send_message(self, msg_body):
        sqs_client = self.get_or_create_client()
        return sqs_client.send_message(QueueUrl=self.sqs_url,
                                            MessageBody=msg_body)

    @raise_exception(catch=ClientError, logger=logger)
    def delete_message(self, receipt_handle):
        sqs_client = self.get_or_create_client()
        return sqs_client.delete_message(QueueUrl=self.sqs_url,
                                              ReceiptHandle=receipt_handle)

    @raise_exception(catch=ClientError, logger=logger)
    def receive_message(self):
        '''
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.receive_message
        '''
        sqs_client = self.get_or_create_client()
        return self.client.receive_message(QueueUrl=self.sqs_url,
                                               AttributeNames=['All'])

