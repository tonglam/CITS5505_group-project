"Service for user views."

from email_validator import EmailNotValidError, validate_email
from werkzeug.datastructures import FileStorage

from app.api.service import (upload_image_service, user_communities_service,
                             user_likes_service, user_posts_service,
                             user_saves_service, user_stats_service,
                             users_records_service)
from app.constants import HttpRequestEnum
from app.models.community import Community
from app.models.user import User, UserStatusEnum
from app.models.user_preference import UserPreference
from app.utils import get_pagination_details


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


def post_data(page: int = 1, per_page: int = 10):
    """Get the user's posts."""

    posts = user_posts_service(page, per_page)
    posts_data = posts.get_json()

    user_posts_data = posts_data["data"]["user_posts"]
    posts_item_data = [
        {"id": post["id"], "title": post["title"]} for post in user_posts_data
    ]

    posts_page = get_pagination_details(
        posts_data["pagination"]["page"],
        posts_data["pagination"]["total_pages"],
        posts_data["pagination"]["total_items"],
    )

    return {"name": "Posts", "data": posts_item_data, "pagination": posts_page}


def like_data(page: int = 1, per_page: int = 10):
    """Get the user's likes."""

    likes = user_likes_service(page, per_page)
    likes_data = likes.get_json()

    user_likes_data = likes_data["data"]["user_likes"]
    likes_item_data = [
        {"id": like["request"]["id"], "title": like["request"]["title"]}
        for like in user_likes_data
    ]

    likes_page = get_pagination_details(
        likes_data["pagination"]["page"],
        likes_data["pagination"]["total_pages"],
        likes_data["pagination"]["total_items"],
    )

    return {
        "name": "Likes",
        "data": likes_item_data,
        "pagination": likes_page,
    }


def history_data(page: int = 1, per_page: int = 10):
    """Get the user's history."""

    histories = users_records_service(page, per_page)
    histories_data = histories.get_json()

    user_histories_data = histories_data["data"]["user_records"]
    histories_item_data = [
        {"id": history["request"]["id"], "title": history["request"]["title"]}
        for history in user_histories_data
    ]

    histories_page = get_pagination_details(
        histories_data["pagination"]["page"],
        histories_data["pagination"]["total_pages"],
        histories_data["pagination"]["total_items"],
    )

    return {
        "name": "History",
        "data": histories_item_data,
        "pagination": histories_page,
    }


def save_data(page: int = 1, per_page: int = 10):
    """Get the user's wishlist."""

    saves = user_saves_service(page, per_page)
    saves_data = saves.get_json()

    user_saves_data = saves_data["data"]["user_saves"]

    saves_item_data = [
        {"id": save["request"]["id"], "title": save["request"]["title"]}
        for save in user_saves_data
    ]

    saves_page = get_pagination_details(
        saves_data["pagination"]["page"],
        saves_data["pagination"]["total_pages"],
        saves_data["pagination"]["total_items"],
    )

    return {"name": "Collects", "data": saves_item_data, "pagination": saves_page}


def stat_data():
    """Get the user's statistics."""

    user_stat = user_stats_service().get_json()
    return user_stat.get("data").get("user_stats")


def display_community_data():
    """Get the user's display communities."""

    user_communities = user_communities_service().get_json()
    user_communities_data = user_communities.get("data").get("user_communities")
    default_data = Community.query.limit(1).all()
    if user_communities_data == []:
        return default_data
    return user_communities_data[0:1]


def get_upload_avatar_url(avatar_file: FileStorage):
    """Get upload avatar url."""

    upload_avatar_response = upload_image_service(avatar_file).get_json()
    if upload_avatar_response.get("code") != HttpRequestEnum.SUCCESS_OK.value:
        return None
    return upload_avatar_response.get("data").get("image_url")
