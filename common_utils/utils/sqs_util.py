import boto3
from botocore.exceptions import ClientError
from src.utils.commons import raise_exception
from src.utils.logger import Logger

logger = Logger('SQSClient')


class SQSClient:

    def __init__(self, sqs_url):
        self.sqs_url = sqs_url
        self.client = boto3.client('sqs')

    @raise_exception(catch=ClientError, logger=logger)
    def send_message(self, msg_body):
        return self.client.send_message(QueueUrl=self.sqs_url,
                                        MessageBody=msg_body)

    @raise_exception(catch=ClientError, logger=logger)
    def delete_message(self, receipt_handle):
        return self.client.delete_message(QueueUrl=self.sqs_url,
                                          ReceiptHandle=receipt_handle)

    @raise_exception(catch=ClientError, logger=logger)
    def receive_message(self):
        '''
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.receive_message
        '''
        return self.client.receive_message(QueueUrl=self.sqs_url,
                                           AttributeNames=['All'])
