import requests

from . import constants
from . import exceptions


class Request(object):
    _headers = None

    def __init__(self, access_token, email, api_version):
        self.access_token = access_token
        self.email = email
        self.api_version = api_version

    @property
    def base_url(self):
        return constants.BASE_URL.format(version=self.api_version)

    @property
    def headers(self):
        if not self._headers:
            self._headers = {
                "Content-Type": constants.CONTENT_TYPE,
                constants.ACCESS_TOKEN_HEADER: self.access_token,
                constants.APPLICATION_HEADER: constants.APPLICATION,
                constants.EMAIL_HEADER: self.email,
            }
        return self._headers

    def _check_response(self, response):
        if not response.status_code == requests.codes.ok:
            exc_class = exceptions.ERROR_CODE_TO_EXCEPTION.get(
                response.status_code, exceptions.ProsperWorksServerException(
                    u"Unknown error", response.status_code,
                )
            )
            try:
                data = response.json()
                raise exc_class(message=data['message'])
            except ValueError:
                raise exc_class
        else:
            try:
                return response.json()
            except ValueError:
                raise exceptions.ProsperWorksBadJson()

    def _check_token_and_email(self):
        if not self.access_token or not self.email:
            raise exceptions.NotConfiguredException()

    def _request(self, endpoint, method, data_kw_name, data=None):
        self._check_token_and_email()
        if data is None:
            data = {}
        url = self.base_url + endpoint

        if data_kw_name == 'kwargs':
            kw = data
        else:
            kw = {data_kw_name: data}

        response = getattr(requests, method)(url, headers=self.headers, **kw)
        return self._check_response(response)

    def get(self, endpoint, params=None):
        return self._request(endpoint, 'get', 'params', data=params)

    def post(self, endpoint, json=None):
        return self._request(endpoint, 'post', 'json', data=json)

    def delete(self, endpoint, kwargs=None):
        return self._request(endpoint, 'delete', 'kwargs', data=kwargs)

    def put(self, endpoint, json=None):
        return self._request(endpoint, 'put', 'json', data=json)
