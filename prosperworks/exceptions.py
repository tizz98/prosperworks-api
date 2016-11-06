class BaseProsperWorksException(Exception):
    pass


class NotConfiguredException(BaseProsperWorksException):
    def __init__(self):
        super(NotConfiguredException, self).__init__(
            "Api not configured. Before making requests, invoke: "
            "prosperworks.api.configure(KEY, EMAIL)."
        )


class ProsperWorksApplicationException(BaseProsperWorksException):
    pass


class ProsperWorksBadJson(ProsperWorksApplicationException):
    pass


class ProsperWorksServerException(BaseProsperWorksException):
    def __init__(self, message, error_code):
        super(ProsperWorksServerException, self).__init__(message)
        self.error_code = error_code

        self.message = u"Server responded with code {}. {}".format(
            self.error_code, self.message
        )


class ProsperWorksBadRequest(ProsperWorksServerException):
    def __init__(self, message=None):
        super(ProsperWorksBadRequest, self).__init__(
            "General client error, possibly malformed request.",
            error_code=400
        )


class ProsperWorksUnauthorizedRequest(ProsperWorksServerException):
    def __init__(self, message=None):
        super(ProsperWorksUnauthorizedRequest, self).__init__(
            "The API key was not authorized (or not API key was found).",
            error_code=401
        )


class ProsperWorksForbiddenRequest(ProsperWorksServerException):
    def __init__(self, message=None):
        super(ProsperWorksForbiddenRequest, self).__init__(
            "The request is not allowed.",
            error_code=403
        )


class ProsperWorksNotFoundRequest(ProsperWorksServerException):
    def __init__(self, message=None):
        super(ProsperWorksNotFoundRequest, self).__init__(
            "The resource was not found.",
            error_code=404
        )


class ProsperWorksUnprocessableRequest(ProsperWorksServerException):
    info_url = "http://www.restpatterns.org/HTTP_Status_Codes/" \
               "422_-_Unprocessable_Entity"

    def __init__(self, message=None):
        super(ProsperWorksUnprocessableRequest, self).__init__(
            "The request is allowed and the resource exists, but is "
            "semantically invalid. %s See %s" % (
                message if message else '',
                self.info_url,
            ),
            error_code=422
        )


class ProsperWorksRateLimitExceeded(ProsperWorksServerException):
    def __init__(self, message=None):
        super(ProsperWorksRateLimitExceeded, self).__init__(
            "The rate limit has been reached for the account. The API allows"
            "600 requests every 10 minutes. For a higher volume, contact "
            "sales@prosperworks.com.",
            error_code=429
        )


class ProsperWorksInternalServerError(ProsperWorksServerException):
    def __init__(self, message=None):
        super(ProsperWorksInternalServerError, self).__init__(
            "You've encountered a bug in ProsperWorks. We'd be very interested"
            " in how you generated this error and would be happy to hear your "
            "feedback at support@prosperworks.com.",
            error_code=500
        )


ERROR_CODE_TO_EXCEPTION = {
    400: ProsperWorksBadRequest,
    401: ProsperWorksUnauthorizedRequest,
    403: ProsperWorksForbiddenRequest,
    404: ProsperWorksNotFoundRequest,
    422: ProsperWorksUnprocessableRequest,
    429: ProsperWorksRateLimitExceeded,
    500: ProsperWorksInternalServerError,
}
