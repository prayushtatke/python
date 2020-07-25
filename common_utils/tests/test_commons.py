from os import path as os_path
from sys import path as sys_path
sys_path.append(os_path.realpath('../'))
import unittest
import common_utils.utils.commons as util


class TestCommonUtils(unittest.TestCase):

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


