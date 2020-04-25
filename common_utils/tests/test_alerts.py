import unittest
from utils.kinesis_util import Kinesis
from utils.alerts import AlertsHandler


class TestAlertsHandler(unittest.TestCase):

    def test_alerts_handler_init(self):
        with self.assertRaises(AssertionError):
            AlertsHandler()

        self.assertIsNotNone(AlertsHandler(stream_name='test_stream', stream_client=Kinesis()))


    def test_alert_payload_format(self):
        actual_payload = AlertsHandler.create_alert_payload('100', 'INVALID_INPUT',
                                                            STR_ARG='STR_VAL',
                                                            INT_ARG=100,
                                                            DICT_ARG={"one": 1, "two":2 }  )

        self.assertTrue(isinstance(actual_payload, dict))
        self.assertEqual('100', actual_payload['err_code'])
        self.assertEqual('INVALID_INPUT', actual_payload['err_msg'])
        self.assertEqual('STR_VAL', actual_payload['STR_ARG'])
        self.assertEqual(100, actual_payload['INT_ARG'])
        self.assertDictEqual({"one": 1, "two":2 }, actual_payload['DICT_ARG'])

