import unittest
from unittest.mock import patch
import utils.commons as util


def raise_exception(raise_expected_exception):
	if raise_expected_exception:
		raise TypeError('RAISED_TYPE_ERROR')
	else:
		raise RuntimeError('')


@util.log_exception(err_msg='PROVIDED_TYPE_ERROR')
def log_exception_err_msg():
	raise_exception(True)


@util.log_exception(catch=TypeError, err_msg='PROVIDED_TYPE_ERROR')
def log_exception_catching_specific_exception(raise_expected_exception):
	raise_exception(raise_expected_exception)


@util.log_exception(catch=(KeyError, TypeError), err_msg='PROVIDED_GENERIC_ERROR')
def log_exception_catch_multiple_exception(raise_expected_exception):
	raise_exception(raise_expected_exception)


@util.raise_exception(err_msg='PROVIDED_TYPE_ERROR')
def raise_exception_err_msg():
	raise_exception(False)


@util.raise_exception(catch=TypeError, throw=Exception, err_msg='PROVIDED_GENERIC_ERROR')
def raise_exception_catching_specific_exception(raise_expected_exception):
	raise_exception(raise_expected_exception)


@util.raise_exception(catch=(KeyError, TypeError), throw=RuntimeError, err_msg='PROVIDED_GENERIC_ERROR')
def raise_exception_catch_multiple_exception(raise_expected_exception):
	raise_exception(raise_expected_exception)


class TestCommonUtils(unittest.TestCase):

	@patch('utils.commons.util_logger')
	def test_log_exception_err_msg(self, mock_logger):

		log_exception_err_msg()
		mock_logger.error.assert_called_with('RAISED_TYPE_ERROR')
		mock_logger.exception.assert_called_with('PROVIDED_TYPE_ERROR')


	@patch('utils.commons.util_logger')
	def test_log_exception_specific_exception(self, mock_logger):

		# test specific exception
		# it will only catch the KeyError, but raise  any other exception.
		with self.assertRaises(RuntimeError):
			log_exception_catching_specific_exception(False)

		log_exception_catching_specific_exception(True)
		mock_logger.error.assert_called_with('RAISED_TYPE_ERROR')
		mock_logger.exception.assert_called_with('PROVIDED_TYPE_ERROR')


	@patch('utils.commons.util_logger')
	def test_log_exception_multiple_exception(self, mock_logger):

		# test specific exception
		# it will only catch the KeyError, but raise  any other exception.
		with self.assertRaises(RuntimeError):
			log_exception_catch_multiple_exception(False)

		log_exception_catch_multiple_exception(True)
		mock_logger.error.assert_called_with('RAISED_TYPE_ERROR')
		mock_logger.exception.assert_called_with('PROVIDED_GENERIC_ERROR')

	@patch('utils.commons.util_logger')
	def test_raise_exception_err_msg(self, mock_logger):
		with self.assertRaises(RuntimeError) as c:
			raise_exception_err_msg()

		mock_logger.error.assert_called_with('')
		self.assertEqual('' ,str(c.exception))


	@patch('utils.commons.util_logger')
	def test_raise_exception_specific_exception(self, mock_logger):

		# test specific exception
		# it will only catch and throw only if internal raised TypeError,
		# but raise any other exception as it is.
		# since the method is throwing RuntimeError, it is not throwing the new exception.
		with self.assertRaises(RuntimeError):
			raise_exception_catching_specific_exception(False)

		with self.assertRaises(Exception) as c:
			raise_exception_catching_specific_exception(True)

		mock_logger.error.assert_called_with('RAISED_TYPE_ERROR')
		self.assertEqual('PROVIDED_GENERIC_ERROR' ,str(c.exception))


	@patch('utils.commons.util_logger')
	def test_raise_exception_multiple_exception(self, mock_logger):

		with self.assertRaises(RuntimeError):
			raise_exception_catching_specific_exception(False)

		with self.assertRaises(Exception) as c:
			raise_exception_catching_specific_exception(True)

		mock_logger.error.assert_called_with('RAISED_TYPE_ERROR')
		self.assertEqual('PROVIDED_GENERIC_ERROR' ,str(c.exception))


	def test_is_empty(self):
		self.assertTrue(util.is_empty(None))
		self.assertTrue(util.is_empty(''))
		self.assertTrue(util.is_empty('    '))
		self.assertTrue(util.is_empty({}))
		self.assertTrue(util.is_empty([]))

		self.assertFalse(util.is_empty(False))
		self.assertFalse(util.is_empty(' A '))
		self.assertFalse(util.is_empty([1]))
		self.assertFalse(util.is_empty({"key" : None}))
		self.assertFalse(util.is_empty(1))
		self.assertFalse(util.is_empty(1.000))
		self.assertFalse(util.is_empty(0))
		self.assertFalse(util.is_empty(0.0))



	def test_is_not_empty(self):
		self.assertFalse(util.is_not_empty(None))
		self.assertFalse(util.is_not_empty(''))
		self.assertFalse(util.is_not_empty(' '))
		self.assertFalse(util.is_not_empty({}))
		self.assertFalse(util.is_not_empty([]))

		self.assertTrue(util.is_not_empty(False))
		self.assertTrue(util.is_not_empty(' A '))
		self.assertTrue(util.is_not_empty([1]))
		self.assertTrue(util.is_not_empty({"key" : None}))
		self.assertTrue(util.is_not_empty(1))
		self.assertTrue(util.is_not_empty(1.000))
		self.assertTrue(util.is_not_empty(0))
		self.assertTrue(util.is_not_empty(0.0))

	def test_find_missing_or_empty_keys(self):
		self.assertIsNone(util.find_missing_or_empty_keys({}, ["one"]))
		self.assertIsNone(util.find_missing_or_empty_keys({"one": 1}, []))

		ip = {"one": 1, "two": 2, "three": 3}
		self.assertListEqual(util.find_missing_or_empty_keys(ip, ["one", "four", "five"]), ["four", "five"])

		ip = {"one": 1, "two": None, "three": '   '}
		self.assertListEqual(util.find_missing_or_empty_keys(ip, ["one", "two", "three"]), ["two", "three"])

	def test_del_dict_keys(self):
		with self.assertRaises(AssertionError):
			util.del_dict_keys({},["one"])

		ip = {"one": 1, "two": 2, "three": 3}
		util.del_dict_keys(ip, ["one", "two", "four"])
		self.assertDictEqual(ip, {"three" : 3})

