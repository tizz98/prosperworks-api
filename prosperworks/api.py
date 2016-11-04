from .request import Request


_key = None
_email = None
requests = Request(_key, _email)


def configure(key, email):
    global _key, _email, requests
    _key = key
    _email = email
    requests = Request(_key, _email)
