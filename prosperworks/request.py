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

    def get(self, endpoint, params=None):
        self._check_token_and_email()
        if params is None:
            params = {}
        url = constants.BASE_URL + endpoint
        response = requests.get(url, params=params, headers=self.headers)
        return self._check_response(response)

    def post(self, endpoint, json=None):
        self._check_token_and_email()
        if json is None:
            json = {}
        url = constants.BASE_URL + endpoint
        response = requests.post(url, json=json, headers=self.headers)
        return self._check_response(response)
