import common_utils.utils.commons as util
import common_utils.utils.aws as aws
from common_utils.utils.decorators import raise_exception
from common_utils.utils.logger import Logger


class Kinesis(aws.Client):
    client_type = 'kinesis'
    logger = Logger('Kinesis')

    def is_stream_exist(self, stream_name):
        """

        :param stream_name:
        :return:
        """
        assert util.is_not_empty(stream_name), \
            "kinesis stream name cannot be empty."

        k_client = self.get_or_create_client()
        exist = False
        try:
            resp = k_client.describe_stream(StreamName=stream_name, Limit=1)
            return resp is not None
        except Exception as e:
            self.logger.exception(str(e))

        return exist


    @raise_exception(logger=logger, err_msg='write_batch(): Failed')
    def write_batch(self, stream_name=None, batch=None):
        """
        :param batch: list of kinesis Records, batch to be published to kinesis
        :param stream_name: kinesis stream name to publish to.
        :return:
        """
        assert util.is_not_empty(stream_name), \
            "Kinesis Stream Name cannot be empty."

        assert batch and len(batch) != 0, \
            "Record list is empty, No records to persist."

        def put_records(stream, records):
            k_client = self.get_or_create_client()
            return k_client.put_records(Records=records, StreamName=stream)

        try:
            return put_records(stream_name, batch)
        except Exception as e:

            self.logger.warning(str(e))
            self.client = None
            return put_records(stream_name, batch)


    @raise_exception(logger=logger, err_msg='write_record(): Failed.')
    def write_record(self, stream_name=None, partition_key=None, record=None):
        """
        :param record: list of kinesis Records, batch to be published to kinesis
        :param stream_name: kinesis stream name to publish to.
        :return:
        """
        assert util.is_not_empty(stream_name), \
            "Kinesis Stream Name cannot be empty."

        assert record is not None, \
            "Record is empty, No records to persist."

        if not partition_key:
            partition_key = str(hash(record))

        def put_record(stream, rec):
            k_client = self.get_or_create_client()
            return k_client.put_record(Data=rec, StreamName=stream, PartitionKey=partition_key)

        try:
            return put_record(stream_name, record)
        except Exception:
            self.client = None
            return put_record(stream_name, record)
