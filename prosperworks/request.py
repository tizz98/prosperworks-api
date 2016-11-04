import requests

import constants
import exceptions


class Request(object):
    _headers = None

    def __init__(self, access_token, email):
        self.access_token = access_token
        self.email = email

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
        url = constants.BASE_URL + endpoint
        response = getattr(requests, method)(
            url,
            headers=self.headers,
            **{data_kw_name: data}
        )
        return self._check_response(response)

    def get(self, endpoint, params=None):
        return self._request(endpoint, 'get', 'params', data=params)

    def post(self, endpoint, json=None):
        return self._request(endpoint, 'post', 'json', data=json)
