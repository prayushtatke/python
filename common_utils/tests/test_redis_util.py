from os import path as os_path
from sys import path as sys_path
sys_path.append(os_path.realpath('../'))
import unittest
import fakeredis
import json
from unittest.mock import patch
from common_utils.utils.redis_util import Redis


class TestRedisUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        server = fakeredis.FakeServer()
        cls.mockclient = fakeredis.FakeStrictRedis(server=server)

    @patch('common_utils.utils.configstore.ConfigStore.get_config')
    def test_init(self, mock_get_config):
        redis = Redis(test_client=self.mockclient)
        self.assertIsNotNone(redis.client)

        # when aws parameter key is provided.
        mock_get_config.return_value = {'redis_host' : 'localhost', 'redis_port' : '6380', 'redis_pass' : 'passwd'}

        # passing test_client so that it doesn't try to create connection.
        redis = Redis(aws_param_name='test_redis_param', namespace='test', test_client=self.mockclient)
        self.assertEqual(redis.host, 'localhost')
        self.assertEqual(redis.port, 6380)
        self.assertEqual(redis.password, 'passwd')

        # when aws secrets is provided
        mock_get_config.return_value = {'redis_pass_v1': 'passwd_v1'}
        redis = Redis(host='localhost_v1', aws_secret_name='test_secrets', aws_secret_pass_key='redis_pass_v1', test_client=self.mockclient)
        self.assertEqual(redis.host, 'localhost_v1')
        self.assertEqual(redis.port, 6379)
        self.assertEqual(redis.password, 'passwd_v1')



    # @unittest.skip
    def test_set_get_hkey_primitives(self):
        redis = Redis(namespace='test', test_client=self.mockclient)

        # single string as key, and string as value
        redis.set_hkey('key_str', 'value')
        value = redis.get_hkey('key_str')
        self.assertEqual(value.get(), 'value')

        # single string as key, and string as value
        redis.set_hkey('key_int', 1)
        value = redis.get_hkey('key_int')

        self.assertEqual(value.get(), 1)

        # single string as key, and string as value
        redis.set_hkey('key_float', 1.5)
        value = redis.get_hkey('key_float')
        self.assertEqual(value.get(), 1.5)

        value = redis.get_hkey('a_non_existent_key')
        self.assertFalse(value.is_present())

    # @unittest.skip
    def test_set_get_hkey_coll(self):
        redis = Redis(namespace='test', test_client=self.mockclient)

        # multiple string to join as key, and stringified dict as value
        dict_val = {'k1': 'v1', 'k2':'v2'}
        redis.set_hkey(['k1', 'k2'], str(dict_val).encode('utf-8'))
        value = redis.get_hkey(['k1', 'k2'])
        self.assertDictEqual(value.get(), dict_val)

        # storing big dict having multiple types of values
        dict_val = {'k1': 'v1', 'k2': 1, 'k3': 2.5, 'k4': {'k4_1': 'v4_1', 'k4_2': 'v4_2'}}
        redis.set_hkey('key_dict', str(dict_val).encode('utf-8'))
        value = redis.get_hkey('key_dict')
        self.assertDictEqual(value.get(), dict_val)

        # storing big dict having multiple types of values as JSON
        redis.set_hkey('key_dict_json', json.dumps(dict_val).encode('utf-8'))
        value = redis.get_hkey('key_dict_json')
        self.assertDictEqual(value.get(), dict_val)

        # storing list
        list_val = ['one', 'two']
        redis.set_hkey('key_list', str(list_val).encode('utf-8'))
        value = redis.get_hkey('key_list')
        self.assertListEqual(value.get(), list_val)

        # storing set
        set_val = {'one', 'two'}
        redis.set_hkey('key_set', str(set_val).encode('utf-8'))
        value = redis.get_hkey('key_set')
        self.assertSetEqual(value.get(), set_val)

    # @unittest.skip
    def test_sethm_getall_hkeys(self):
        redis = Redis(namespace='test2', test_client=self.mockclient)

        # single string as key, and string as value
        hm = { 'key:str:w123': 'v1', 'key:int': 1, 'key:float': 1.5}
        redis.set_hkeys(hm)

        self.assertTrue(redis.exist_hkey('key:str:w123'))
        self.assertTrue(redis.exist_hkey('key:int'))
        self.assertTrue(redis.exist_hkey('key:float'))

        # storing complex types
        list_val = ['one', 'two']
        dict_val = {'k1': 'v1', 'k2': 1, 'k3': 2.5, 'k4': {'k4_1': 'v4_1', 'k4_2': 'v4_2'}}
        redis.set_hkey('key_list', str(list_val).encode('utf-8'))
        redis.set_hkey('key_dict', json.dumps(dict_val).encode('utf-8'))

        hm.update({'key_list': list_val, 'key_dict': dict_val})
        result = redis.getall_hkeys()
        self.assertDictEqual(hm, result.get())

        result = redis.getall_hkeys(namespace='a_non_existent_ns')
        self.assertFalse(result.is_present())

    def test_sethm_get_hkeys(self):
        redis = Redis(namespace='test2', test_client=self.mockclient)

        # single string as key, and string as value
        hm = {'key:str:w123': 'v1', 'key:int': 1, 'key:float': 1.5}
        redis.set_hkeys(hm)

        result = redis.get_hkeys(["key:str:w123","key:int","key:float"])
        self.assertDictEqual(hm, result.get())

        hm = {'key:str:w123': 'v1', 'key:int': '1', 'key:float': '1.5'}
        result = redis.get_hkeys(["key:str:w123", "key:int", "key:float"], eval=False)
        self.assertDictEqual(hm, result.get())


    # @unittest.skip
    def test_sethm_getall_hkeys_pattern(self):
        redis = Redis(namespace='test3', test_client=self.mockclient)

        # single string as key, and string as value
        hm = {
                'key_111:abc:111': 'v1',
                'key_111:def:222': 'v2',
                'key_222:abc:333': 'v3',
                'key_222:ghi:111': 'v4'
            }
        redis.set_hkeys(hm)

        keys_prefix = redis.getall_hkeys(key_prefix='key_111')
        self.assertTrue(keys_prefix.is_present())
        keys_prefix = keys_prefix.get()
        self.assertEqual(len(keys_prefix), 2)
        self.assertEqual(keys_prefix['key_111:abc:111'], 'v1')
        self.assertEqual(keys_prefix['key_111:def:222'], 'v2')

        keys_suffix = redis.getall_hkeys(key_suffix='111')
        self.assertTrue(keys_suffix.is_present())
        keys_suffix = keys_suffix.get()
        self.assertEqual(len(keys_suffix), 2)
        self.assertEqual(keys_suffix['key_111:abc:111'], 'v1')
        self.assertEqual(keys_suffix['key_222:ghi:111'], 'v4')

        keys_contains = redis.getall_hkeys(key_contains='abc')
        self.assertTrue(keys_contains.is_present())
        keys_contains = keys_contains.get()
        self.assertEqual(len(keys_contains), 2)
        self.assertEqual(keys_contains['key_111:abc:111'], 'v1')
        self.assertEqual(keys_contains['key_222:abc:333'], 'v3')


if __name__ == "__main__":
    unittest.main()
