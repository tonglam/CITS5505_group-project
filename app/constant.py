"""Constant file for the application."""

import enum


class HttpRequstErrorEnum(enum.Enum):
    """Enum for HTTP request error."""

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class UserRecordEnum(enum.Enum):
    """Enum for user record."""

    REQUEST = "REQUEST"
    REPLY = "REPLY"
    VIEW = "VIEW"
    LIKE = "LIKE"
    SAVE = "SAVE"


class UserStatusEnum(enum.Enum):
    """Enum for user status."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


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
