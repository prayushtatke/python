from os import path as os_path
from sys import path as sys_path
sys_path.append(os_path.realpath('../'))
import unittest
from unittest.mock import patch
import common_utils.utils.decorators as dc


def raise_exceptn(raise_expected_exception):
	if raise_expected_exception:
		raise TypeError('RAISED_TYPE_ERROR')
	else:
		raise RuntimeError('')

@dc.log_exception(err_msg='PROVIDED_TYPE_ERROR')
def log_exception_err_msg():
	raise_exceptn(True)


@dc.log_exception(catch=TypeError, err_msg='PROVIDED_TYPE_ERROR')
def log_exception_catching_specific_exception(raise_expected_exception):
	raise_exceptn(raise_expected_exception)


@dc.log_exception(catch=(KeyError, TypeError), err_msg='PROVIDED_GENERIC_ERROR')
def log_exception_catch_multiple_exception(raise_expected_exception):
	raise_exceptn(raise_expected_exception)


@dc.raise_exception(err_msg='PROVIDED_TYPE_ERROR')
def raise_exception_err_msg():
	raise_exceptn(False)

@dc.raise_exception(catch=TypeError, throw=Exception, err_msg='PROVIDED_GENERIC_ERROR')
def raise_exception_catching_specific_exception(raise_expected_exception):
	raise_exceptn(raise_expected_exception)

@dc.raise_exception(catch=(KeyError, TypeError), throw=RuntimeError, err_msg='PROVIDED_GENERIC_ERROR')
def raise_exception_catch_multiple_exception(raise_expected_exception):
	raise_exceptn(raise_expected_exception)

@dc.return_opt_empty_when_error()
def raise_exception_for_opt_empty_test():
    return raise_exceptn(False)


class TestDecorators(unittest.TestCase):

    @patch('common_utils.utils.decorators._logger.error')
    def test_log_exception_err_msg(self, mock_logger):
        log_exception_err_msg()
        # Note: it is only taking the last method call.

        # mock_logger.assert_called_with('PROVIDED_TYPE_ERROR')
        mock_logger.assert_called_with('RAISED_TYPE_ERROR')


    @patch('common_utils.utils.decorators._logger.error')
    def test_log_exception_specific_exception(self, mock_logger):
        # test specific exception
        # it will only catch the KeyError, but raise  any other exception.
        with self.assertRaises(RuntimeError):
            log_exception_catching_specific_exception(False)

        log_exception_catching_specific_exception(True)
        mock_logger.assert_called_with('RAISED_TYPE_ERROR')

    @patch('common_utils.utils.decorators._logger.error')
    def test_log_exception_multiple_exception(self, mock_logger):
        # test specific exception
        # it will only catch the KeyError, but raise  any other exception.
        with self.assertRaises(RuntimeError):
            log_exception_catch_multiple_exception(False)

        log_exception_catch_multiple_exception(True)
        mock_logger.assert_called_with('RAISED_TYPE_ERROR')

    @patch('common_utils.utils.decorators._logger.error')
    def test_raise_exception_err_msg(self, mock_logger):
        with self.assertRaises(RuntimeError) as c:
            raise_exception_err_msg()

        mock_logger.assert_called_with('')
        self.assertEqual('', str(c.exception))

    @patch('common_utils.utils.decorators._logger.error')
    def test_raise_exception_specific_exception(self, mock_logger):
        # test specific exception
        # it will only catch and throw only if internal raised TypeError,
        # but raise any other exception as it is.
        # since the method is throwing RuntimeError, it is not throwing the new exception.
        with self.assertRaises(RuntimeError):
            raise_exception_catching_specific_exception(False)

        with self.assertRaises(Exception) as c:
            raise_exception_catching_specific_exception(True)

        mock_logger.assert_called_with('RAISED_TYPE_ERROR')
        self.assertEqual('PROVIDED_GENERIC_ERROR', str(c.exception))

    @patch('common_utils.utils.decorators._logger.error')
    def test_raise_exception_multiple_exception(self, mock_logger):
        with self.assertRaises(RuntimeError):
            raise_exception_catching_specific_exception(False)

        with self.assertRaises(Exception) as c:
            raise_exception_catching_specific_exception(True)

        mock_logger.assert_called_with('RAISED_TYPE_ERROR')
        self.assertEqual('PROVIDED_GENERIC_ERROR', str(c.exception))


    def test_return_opt_empty_when_error(self):
        from common_utils.utils.optional import Optional
        opt : Optional = raise_exception_for_opt_empty_test()
        self.assertFalse(opt.is_present())

