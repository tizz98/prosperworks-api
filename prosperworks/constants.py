__version__ = "0.1.6"

# Headers
# values
CONTENT_TYPE = "application/json"
APPLICATION = "developer_api"

# keys
ACCESS_TOKEN_HEADER = "X-PW-AccessToken"
APPLICATION_HEADER = "X-PW-Application"
EMAIL_HEADER = "X-PW-UserEmail"

# Order by most recent first, default will be API_VERSIONS[0]
API_VERSIONS = (
    "v1",
)
BASE_URL = "https://api.prosperworks.com/developer_api/{version}/"


CACHE_LIFE = 60 * 60  # 1 hour
