from enum import Enum
class ErrCode(Enum):
	INVALID_INPUT = '100'
	MISSING_REQUIRED_INPUT = '101'
	INVALID_DATA_FORMAT = '102'
	UNKNOWN_ERR = '300'


class InvalidInputException(Exception):
	err_code = ErrCode.INVALID_INPUT

	def __init__(self, err_msg):
		self.err_msg = err_msg


class MissingRequiredInput(InvalidInputException):
	err_code = ErrCode.MISSING_REQUIRED_INPUT


class InvalidDataFormat(InvalidInputException):
	err_code = ErrCode.INVALID_DATA_FORMAT


class UnknownAppException(Exception):
	err_code = ErrCode.UNKNOWN_ERR

	def __init__(self, err_msg):
		self.err_msg = err_msg