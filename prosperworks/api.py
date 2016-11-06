from .request import Request
from .constants import API_VERSIONS


_key = None
_email = None
_api_version = API_VERSIONS[0]
requests = Request(_key, _email, _api_version)


def configure(key, email, api_version=API_VERSIONS[0]):
    global _key, _email, _api_version, requests
    _key = key
    _email = email
    _api_version = api_version
    requests = Request(_key, _email, _api_version)
