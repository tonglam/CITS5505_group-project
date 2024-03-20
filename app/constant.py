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


class OAuthProviderEnum(enum.Enum):
    """Enum for OAuth provider."""

    GOOGLE = "google"
    GITHUB = "github"
