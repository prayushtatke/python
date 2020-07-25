from os import path as os_path
from sys import path as sys_path
sys_path.append(os_path.realpath('../'))
import unittest
from common_utils.utils.optional import Optional, OptionalNoneValueError

class TestOptional(unittest.TestCase):

    def test_is_present(self):
        opt = Optional.empty()
        self.assertFalse(opt.is_present())

        opt_actual_values = [ Optional(v) for v in [None, '', [], {}]]
        for opt in opt_actual_values:
            self.assertFalse(opt.is_present())

        opt_actual_values = [Optional(v) for v in ['text', ['some'], {'key' : 'val'}, 0 , 0.0]]
        for opt in opt_actual_values:
            self.assertTrue(opt.is_present())

    def test_get(self):
        with self.assertRaises(OptionalNoneValueError):
            Optional.empty().get()

        opt = Optional('one')
        self.assertTrue(opt.is_present())
        self.assertEqual('one', opt.get())

        fl = 0.001
        opt = Optional(fl)
        self.assertEqual(fl, opt.get())

        l = ['one', 'two']
        opt = Optional(l)
        self.assertListEqual(l, opt.get())

        m = {'one' : 1}
        opt = Optional(m)
        self.assertDictEqual(m, opt.get())

    def test_get_or_else(self):
        opt = Optional.empty()
        self.assertFalse(opt.is_present())
        self.assertEqual('one', opt.get_or_else('one'))

    def test_get_or_raise(self):
        opt = Optional.empty()
        self.assertFalse(opt.is_present())
        with self.assertRaises(KeyError):
            opt.get_or_raise(KeyError, 'KEY_NOT_FOUND')






