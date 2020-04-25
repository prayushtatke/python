import sys
import os
sys.path.append(os.path.realpath('../'))
sys.path.append(os.path.realpath('./'))
from src.status.status import Status, StatusFactory, StatusImplementationError
import unittest
import fakeredis
from datetime import datetime
from common_utils.utils.redis_util import Redis


class TestStatusInterface(unittest.TestCase):
    def setUp(self):
        server = fakeredis.FakeServer()
        self.mockclient = fakeredis.FakeStrictRedis(server=server)
        config = {
        }
        mock_client = Redis(host='localhost', test_client=self.mockclient)
        self.interface = Status(config, mock_client)

    def test_status_factory_implementer(self):
        impl = StatusFactory.get_status_impl('exist_impl')
        self.assertEqual(, impl)

    def test_status_factory(self):
        with self.assertRaises(StatusImplementationError):
            StatusFactory.get_status_impl('random_name')



if __name__ == "__main__":
    unittest.main()
