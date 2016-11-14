import unittest

from prosperworks import utils
from prosperworks import exceptions


class TestValidateFields(unittest.TestCase):
    def test_invalid_validate_fields(self):
        fields_to_validate = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        valid_fields = ['d', 'e', 'f']

        with self.assertRaises(exceptions.ProsperWorksApplicationException):
            utils.validate_fields(fields_to_validate, valid_fields)

    def test_valid_validate_fields(self):
        fields_to_validate = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        valid_fields = ['a', 'b', 'c', 'd']
        utils.validate_fields(fields_to_validate, valid_fields)


class TestDataClass(unittest.TestCase):
    def test_simple_kwargs(self):
        data = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        obj = utils.Data(**data)
        self.assertEqual(obj.a, 1)
        self.assertEqual(obj.b, 2)
        self.assertEqual(obj.c, 3)

    def test_complex_kwargs(self):
        data = {
            'a': {
                'nested': 1,
            },
            'b': 2
        }
        obj = utils.Data(**data)
        self.assertTrue(isinstance(obj.a, utils.Data))
        self.assertEqual(obj.a.nested, 1)

    def test_no_kwargs_populate(self):
        data = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        obj = utils.Data()
        self.assertFalse(hasattr(obj, 'a'))
        self.assertFalse(hasattr(obj, 'b'))
        self.assertFalse(hasattr(obj, 'c'))

        obj.populate(data=data)

        self.assertEqual(obj.a, 1)
        self.assertEqual(obj.b, 2)
        self.assertEqual(obj.c, 3)


class TestLazyProperty(unittest.TestCase):
    def setUp(self):
        class Test(object):
            @utils.lazy_property
            def a(self):
                return self.a_id

            a_id = 123

        self.cls = Test

    def test_not_loaded(self):
        instance = self.cls()
        self.assertEqual(instance.a_id, 123)
        with self.assertRaises(KeyError):
            _ = instance.__dict__['a']
        self.assertEqual(instance.a, 123)


class TestAbstractMixin(unittest.TestCase):
    def setUp(self):
        class Test(utils.AbstractMixin):
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

        self.cls = Test

    def test_args(self):
        instance = self.cls()
        self.assertEqual(instance.args, tuple())

        i2 = instance(1, 2, 3)
        self.assertEqual(instance.args, tuple())
        self.assertEqual(i2.args, (1, 2, 3))

    def test_kwargs(self):
        instance = self.cls()
        self.assertDictEqual(instance.kwargs, {})

        i2 = instance(a=1, b=2, c=3)
        self.assertDictEqual(instance.kwargs, {})
        self.assertDictEqual(i2.kwargs, {'a': 1, 'b': 2, 'c': 3})
