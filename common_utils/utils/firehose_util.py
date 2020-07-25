import common_utils.utils.aws as aws
import common_utils.utils.commons as util
from common_utils.utils.decorators import raise_exception
from common_utils.utils.logger import Logger

class Firehose(aws.Client):

	client_type = 'firehose'
	logger = Logger('Firehose')

	@raise_exception(logger=logger, err_msg='write_record(): Failed.')
	def write_record(self, stream_name=None, record=None):
		"""
		:param stream_name: firehose stream name to publish to.
		:param record: , data in bytes to be published to firehose
		:return: firehose response
		"""
		assert util.is_not_empty(stream_name), \
			"Kinesis Firehose StreamName cannot be empty."

		assert record is not None, \
			"Record cannot be empty."

		f_client = self.get_or_create_client()
		return f_client.put_record(
			DeliveryStreamName=stream_name,
			Record={
				'Data': record
			}
		)


	@raise_exception(logger=logger, err_msg='write_batch(): Failed.')
	def write_batch(self, stream_name=None, batch=None):
		"""
		:param stream_name: firehose stream name to publish to.
		:param data_bytes: , data in bytes to be published to firehose
		:return: firehose response
		"""
		assert util.is_not_empty(stream_name), \
			"Kinesis Firehose StreamName cannot be empty."

		assert batch and len(batch) != 0, \
			"Batch cannot be empty."

		f_client = self.get_or_create_client()
		record_batch = [ {'Data': data} for data in batch ]	
		return f_client.put_record_batch(
			DeliveryStreamName=stream_name,
			Records=record_batch
		)

