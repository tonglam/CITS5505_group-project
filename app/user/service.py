"Service for user views."

from email_validator import EmailNotValidError, validate_email

from app.models.user import User, UserStatusEnum
from app.models.user_preference import UserPreference


def validate_username(username: str) -> None:
    """Update username."""

    if not isinstance(username, str):
        raise TypeError("[username] must be a string")

    if User.query.filter_by(username=username).first() is not None:
        raise ValueError("[username] already exists")


def validate_email_addr(email: str) -> None:
    """Update email."""

    if not isinstance(email, str):
        raise TypeError("[email] must be a string")

    try:
        validate_email(email)
    except EmailNotValidError as e:
        raise ValueError("[email] is invalid") from e


def validate_avatar_url(avatar_url: str) -> None:
    """Update avatar url."""

    if not isinstance(avatar_url, str):
        raise TypeError("[avatar_url] must be a string")


def validate_use_google(use_google: bool) -> None:
    """Update use google."""

    if not isinstance(use_google, bool):
        raise TypeError("[use_google] must be a boolean")


def validate_use_github(use_github: bool) -> None:
    """Update use github."""

    if not isinstance(use_github, bool):
        raise TypeError("[use_github] must be a boolean")


def validate_security_question(security_question: str) -> None:
    """Update security question."""

    if not isinstance(security_question, str):
        raise TypeError("[security_question] must be a string")


def validate_security_answer(security_answer: str) -> None:
    """Update security answer."""

    if not isinstance(security_answer, str):
        raise TypeError("[security_answer] must be a string")


def validate_status(status: str) -> None:
    """Update status."""

    if not isinstance(status, str):
        raise TypeError("[status] must be a string")

    if status not in [status.value for status in UserStatusEnum]:
        raise ValueError("[status] is invalid")


def update_user_data(user_entity: User, update_data: dict) -> User:
    """Create user update data."""

    for key, value in update_data.items():
        if key == "username":
            validate_username(value)
            user_entity.username = value
        elif key == "email":
            validate_email_addr(value)
            user_entity.email = value
        elif key == "avatar_url":
            validate_avatar_url(value)
            user_entity.avatar_url = value
        elif key == "use_google":
            validate_use_google(value)
            user_entity.use_google = value
        elif key == "use_github":
            validate_use_github(value)
            user_entity.use_github = value
        elif key == "security_question":
            validate_security_question(value)
            user_entity.security_question = value
        elif key == "security_answer":
            validate_security_answer(value)
            user_entity.security_answer = value
        elif key == "status":
            validate_status(value)
            user_entity.status = value

    return user_entity


def update_user_preference_data(
    user_preference_entity: UserPreference, update_data: dict
) -> UserPreference:
    """Create user preference update data."""

    for key, value in update_data.items():
        if key == "communities":
            validate_communities(value)
            user_preference_entity.communities = value
        elif key == "interests":
            validate_interests(value)
            user_preference_entity.interests = value

    return user_preference_entity


def validate_communities(communities: str) -> None:
    """Update communities."""

    if not isinstance(communities, str):
        raise TypeError("[communities] must be a string")


def validate_interests(interests: str) -> None:
    """Update interests."""

    if not isinstance(interests, str):
        raise TypeError("[interests] must be a string")
