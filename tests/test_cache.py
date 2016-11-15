import time
import unittest

from prosperworks import cache


class TestCacheClass(unittest.TestCase):
    def setUp(self):
        self.short_cache = cache.Cache(max_life=1)  # 1s
        self.long_cache = cache.Cache()  # 1 hour

    def test_get_set(self):
        self.short_cache.set("a", 1)
        time.sleep(1.1)
        self.assertEqual(self.short_cache.get("a", default=2), 2)

        self.long_cache.set("b", "test")
        time.sleep(1.1)
        self.assertEqual(self.long_cache.get("b"), "test")

    def test_get_or_set(self):
        def func():
            return 'abc'

        self.assertEqual(self.short_cache.get_or_set("key1", func), "abc")
        time.sleep(1.1)
        self.assertIsNone(self.short_cache.get("key1"))

        self.assertEqual(self.long_cache.get_or_set("key2", func), "abc")
        time.sleep(1.1)
        self.assertEqual(self.long_cache.get("key2"), "abc")
