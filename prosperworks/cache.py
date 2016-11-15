import time

from .constants import CACHE_LIFE


class Cache(object):
    def __init__(self, max_life=CACHE_LIFE):
        self.max_life = max_life
        self._cache = {}

    def get(self, key, default=None):
        if key in self._cache:
            value = self._cache[key]
            if time.time() - value[1] < self.max_life:
                return value[0]
            else:
                del self._cache[key]
                return default

    def set(self, key, value):
        self._cache[key] = (value, time.time())

    def get_or_set(self, key, func):
        value = self.get(key)
        if not value:
            value = func()
            self.set(key, value)
        return value
