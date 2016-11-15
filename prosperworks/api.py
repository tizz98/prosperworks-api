from .cache import Cache
from .constants import API_VERSIONS, CACHE_LIFE
from .request import Request


_key = None
_email = None
_api_version = API_VERSIONS[0]
_cache_life = CACHE_LIFE
cache = Cache(max_life=_cache_life)
requests = Request(_key, _email, _api_version)


def configure(key, email, api_version=API_VERSIONS[0], cache_life=CACHE_LIFE):
    global _key, _email, _api_version, requests, _cache_life, cache
    _key = key
    _email = email
    _api_version = api_version
    _cache_life = cache_life
    cache = Cache(max_life=_cache_life)
    requests = Request(_key, _email, _api_version)
