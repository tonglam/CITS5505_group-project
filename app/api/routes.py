"""Routes for api."""

from dataclasses import asdict, dataclass

from flask import jsonify

from app.api import api_bp
from app.constant import HttpRequstEnum
from app.models.category import Category
from app.models.tag import Tag
from app.models.user import User
from app.models.user_preference import UserPreference
from app.models.user_record import UserRecord


@dataclass
class ApiResponse:
    """Api response template dat class."""

    code: HttpRequstEnum = HttpRequstEnum.SUCCESS_OK.value
    data: object = None
    message: str = "success"

    def json(self) -> str:
        """Convert the response to JSON."""
        return jsonify(asdict(self))


# Api for auth module.


# Api for user module.


@api_bp.route("/users/<user_id>", methods=["GET"])
def users(user_id: str) -> ApiResponse:
    """Get a user by id."""

    user_entity = User.query.get(user_id)
    if user_entity is None:
        return ApiResponse(HttpRequstEnum.BAD_REQUEST.value, data={"user": ""}).json()
    return ApiResponse(data={"user": user_entity.to_dict()}).json()


@api_bp.route("/users/records/<user_id>", methods=["GET"])
def user_records(user_id: str) -> ApiResponse:
    """Get records of a user by id."""

    user_record_entities = UserRecord.query.filter_by(user_id=user_id).all()
    user_record_collection = [record.to_dict() for record in user_record_entities]
    return ApiResponse(data={"records": user_record_collection}).json()


@api_bp.route("/users/preferences/<user_id>", methods=["GET"])
def user_preferences(user_id: str) -> ApiResponse:
    """Get preferences of a user by id."""

    user_preference_entities = UserPreference.query.filter_by(user_id=user_id).all()
    user_preferences_collection = [
        preference.to_dict() for preference in user_preference_entities
    ]
    return ApiResponse(data={"preferences": user_preferences_collection}).json()


# Api for community module.


# Api for popular module.


# Api for post module.


# Api for search module.


# Api for notice module.


# Api for others.


@api_bp.route("/categories", methods=["GET"])
def categories() -> ApiResponse:
    """Get all categories."""

    category_entities = Category.query.all()
    category_collection = [category.to_dict() for category in category_entities]
    return ApiResponse(data={"categories": category_collection}).json()


@api_bp.route("/categories/<category_id>", methods=["GET"])
def category(category_id: int) -> ApiResponse:
    """Get a category by id."""

    category_entity = Category.query.get(category_id)
    if category_entity is None:
        return ApiResponse(
            HttpRequstEnum.BAD_REQUEST.value, data={"category": ""}
        ).json()
    return ApiResponse(data={"category": category_entity.to_dict()}).json()


@api_bp.route("/tags", methods=["GET"])
def tags() -> ApiResponse:
    """Get all tags."""

    tag_entities = Tag.query.all()
    tags_collection = [tag.to_dict() for tag in tag_entities]
    return ApiResponse(data={"tags": tags_collection}).json()


@api_bp.route("/tags/<tag_id>", methods=["GET"])
def tag(tag_id: int) -> ApiResponse:
    """Get a tag by id."""

    tag_entity = Tag.query.get(tag_id)
    if tag_entity is None:
        return ApiResponse(HttpRequstEnum.BAD_REQUEST.value, data={"tag": ""}).json()
    return ApiResponse(data={"tag": tag_entity.to_dict()}).json()
