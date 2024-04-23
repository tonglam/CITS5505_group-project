"""Constant file for the application."""

import enum


class HttpRequstEnum(enum.Enum):
    """Enum for HTTP request."""

    SUCCESS_OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503


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
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
CALLBACK_URL = "callback_url"
RESPONSE_TYPE = "code"
SCOPES = "scopes"
AUTHORIZATION_CODE = "authorization_code"
AUTHORIZE_URL = "authorize_url"
TOKEN_URL = "token_url"


class OAuthProviderEnum(enum.Enum):
    """Enum for OAuth provider."""

    GOOGLE = "google"
    GITHUB = "github"


# Gravatar
GRAVATAR_URL = "https://www.gravatar.com/avatar/"

# Flask Globlal Variable
G_USER = "user"
G_NOTICE_NUM = "notice_num"

# Max notice number
MAX_NOTICE_NUM = 99
