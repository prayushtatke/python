import unittest
from common_utils.utils import time_utils as tu

class TestTimeUtils(unittest.TestCase):
    pass

    def test_is_ts_diff_limit_exceeded(self):
        # test function with int parameters, with default unit as Seconds
        val = tu.is_ts_diff_limit_exceeded(1593511320, 1593511200, 90)
        self.assertTrue(val)

        # test function with int parameters, with unit as minutes
        val = tu.is_ts_diff_limit_exceeded(1593513360, 1593511200, 30, tu.TimeUnit.MINS)
        self.assertTrue(val)

        val = tu.is_ts_diff_limit_exceeded(1593512940, 1593511200, 30, tu.TimeUnit.MINS)
        self.assertFalse(val)

        # test function with int parameters, with unit as hours
        val = tu.is_ts_diff_limit_exceeded(1593514920, 1593511200, 1, tu.TimeUnit.HRS)
        self.assertTrue(val)

        # test function with int parameters, with unit as days
        val = tu.is_ts_diff_limit_exceeded(1593511260, 1593424800, 1, tu.TimeUnit.DAYS)
        self.assertTrue(val)

        # test function with str parameters
        val = tu.is_ts_diff_limit_exceeded('2020-06-30 10:45:00', '2020-06-30 10:00:00', 30, tu.TimeUnit.MINS)
        self.assertTrue(val)

        # test function by passing 0 as threshold
        val = tu.is_ts_diff_limit_exceeded(1593511260, 1593511260, 0, tu.TimeUnit.DAYS)
        self.assertTrue(val)

    def test_to_datetime(self):
        in_date_ist = "2020-07-21 17:30:00"
        expected_utc = "2020-07-21 12:00:00"

        val = tu.to_datetime(in_date_ist, fmt="%Y-%m-%d %H:%M:%S", in_tz_offset="+0530", tz_out="UTC")
        self.assertEqual(val.strftime("%Y-%m-%d %H:%M:%S"), expected_utc)

        val = tu.to_datetime(in_date_ist, fmt="%Y-%m-%d %H:%M:%S", in_tz_offset="+05:30", out_tz_offset="+00:00")
        self.assertEqual(val.strftime("%Y-%m-%d %H:%M:%S"), expected_utc)

        # val = tu.to_datetime(in_date_ist, fmt="%Y-%m-%d %H:%M:%S", tz_in="Asia/Kolkata", tz_out="UTC")
        # print(val.strftime("%Y-%m-%d %H:%M:%S %Z %z"))
        #
        # val = tu.to_datetime(in_date_utc, fmt="%Y-%m-%d %H:%M:%S", tz_in="UTC", tz_out="Asia/Kolkata")
        # print(val.strftime("%Y-%m-%d %H:%M:%S %Z %z"))
