"""Constant file for the application."""

import enum


class EnvironmentEnum(enum.Enum):
    """Enum for environment."""

    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class HttpRequestEnum(enum.Enum):
    """Enum for HTTP request."""

    SUCCESS_OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    GONE = 410
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class FlashAlertTypeEnum(enum.Enum):
    """Enum for flash alert type."""

    PRIMARY = "alert-primary"
    SECONDARY = "alert-secondary"
    SUCCESS = "alert-success"
    DANGER = "alert-danger"
    WARNING = "alert-warning"
    INFO = "alert-info"
    LIGHT = "alert-light"
    DARK = "alert-dark"


# OAuth provider
OAUTH2_PROVIDERS = "OAUTH2_PROVIDERS"
OAUTH2_STATE = "oauth2_state"
CLIENT_ID = "oauth_client_id"
CLIENT_SECRET = "oauth_client_secret"
REDIRECT_URI = "oauth_redirect_uri"
AUTH_URL = "oauth_auth_url"
TOKEN_URL = "oauth_token_url"
USER_INFO_URL = "oauth_user_info_url"
SCOPE_PROFILE = "oauth_scope_profile"
SCOPE_EMAIL = "oauth_scope_email"
RESPONSE_TYPE = "code"
SCOPES = "scopes"
AUTHORIZATION_CODE = "authorization_code"
AUTHORIZE_URL = "authorize_url"


class OAuthProviderEnum(enum.Enum):
    """Enum for OAuth provider."""

    GOOGLE = "google"
    GITHUB = "github"


# Gravatar
GRAVATAR_URL = "https://www.gravatar.com/avatar/"

# Dicebear Avatar
DICEBEAR_AVATAR_URL = "https://api.dicebear.com/8.x/pixel-art/jpg?seed="

# Flask Global Variable
G_USER = "user"
G_POST_STAT = "post_stat"
G_NOTICE_NUM = "notice_num"
G_NOTICE = "notices"

# Max notice number
MAX_NOTICE_NUM = 99

# Home page popular post number
POPULAR_POST_NUM = 5

# Home page community option number
COMMUNITY_OPTION_NUM = 20

# Scheduler job interval
JOB_INTERVAL = {
    "create_request": 300,  # 5 minutes
    "create_reply": 300,  # 5 minutes
    "create_user": 300,  # 5 minutes
    "create_user_record": 300,  # 5 minutes
    "create_user_like": 300,  # 5 minutes
    "create_user_save": 300,  # 5 minutes
    "update_trending": 600,  # 10 minutes
}

# Max limitation
USER_MAX_NUM = 999
REQUEST_MAX_NUM = 9999
REPLY_MAX_NUM = 9999
USER_RECORD_MAX_NUM = 99999
USER_LIKE_MAX_NUM = 99999
USER_SAVE_MAX_NUM = 99999

# Top data number
TOP_DATA_NUM = 5
TOP_COMMUNITY_NUM = 4

# Display community number
DISPLAY_COMMUNITY_NUM = 8
