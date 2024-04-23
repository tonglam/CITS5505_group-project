"""Routes for api."""

from dataclasses import asdict, dataclass

from flask import jsonify, request
from flask_login import login_required

from app.api import api_bp
from app.constants import HttpRequstEnum
from app.extensions import db
from app.models.category import Category
from app.models.tag import Tag
from app.models.user import User
from app.models.user_preference import UserPreference
from app.models.user_record import UserRecord

from .service import update_user_data, update_user_preference_data


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


@api_bp.route("/users/<user_id>", methods=["GET", "PUT"])
@login_required
def users(user_id: str) -> ApiResponse:
    """Get a user by id."""

    user_entity = User.query.get(user_id)

    if user_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="user not found"
        ).json()

    if request.method == "GET":
        return ApiResponse(data={"user": user_entity.to_dict()}).json()

    if request.method == "PUT":
        request_data = request.json

        if request_data is None or request_data == {}:
            return ApiResponse(
                HttpRequstEnum.BAD_REQUEST.value, message="request data is empty"
            ).json()

        # update user data
        try:
            update_user_entity = update_user_data(user_entity, request_data)
        except (TypeError, ValueError) as e:
            return ApiResponse(HttpRequstEnum.BAD_REQUEST.value, message=str(e)).json()

        # update user into database
        db.session.commit()

        return ApiResponse(
            data={"user": update_user_entity.to_dict()}, message="user update success"
        ).json()

    return ApiResponse(
        HttpRequstEnum.METHOD_NOT_ALLOWED.value, message="method not allowed"
    ).json()


@api_bp.route("/users/records/<user_id>", methods=["GET"])
@login_required
def user_records(user_id: str) -> ApiResponse:
    """Get records of a user by id."""

    user_record_entities = UserRecord.query.filter_by(user_id=user_id).all()
    user_record_collection = [record.to_dict() for record in user_record_entities]

    return ApiResponse(data={"records": user_record_collection}).json()


@api_bp.route("/users/records/<int:record_id>", methods=["DELETE"])
@login_required
def del_users_record(record_id: int) -> ApiResponse:
    """Delete record by id."""

    record_entity = UserRecord.query.get(record_id)

    if record_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="record not found"
        ).json()

    db.session.delete(record_entity)
    db.session.commit()

    return ApiResponse(
        HttpRequstEnum.NO_CONTENT.value, message="record delete success"
    ).json()


@api_bp.route("/users/preferences/<user_id>", methods=["GET"])
@login_required
def user_preferences(user_id: str) -> ApiResponse:
    """Get preferences of a user by id."""

    user_preference_entities = UserPreference.query.filter_by(user_id=user_id).all()
    user_preferences_collection = [
        preference.to_dict() for preference in user_preference_entities
    ]

    return ApiResponse(data={"preferences": user_preferences_collection}).json()


@api_bp.route("/users/preferences/<int:preference_id>", methods=["PUT"])
@login_required
def user_preference(preference_id: int):
    """Update a preference by id."""

    user_preference_entity = UserPreference.query.get(preference_id)
    if user_preference_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="preference not found"
        ).json()

    if request.method == "PUT":
        request_data = request.json

        if request_data is None or request_data == {}:
            return ApiResponse(
                HttpRequstEnum.BAD_REQUEST.value, message="request data is empty"
            ).json()

        # update user preference data
        try:
            update_user_preference_entity = update_user_preference_data(
                user_preference_entity, request_data
            )
        except (TypeError, ValueError) as e:
            return ApiResponse(HttpRequstEnum.BAD_REQUEST.value, message=str(e)).json()

        # update user preference into database
        db.session.commit()

        return ApiResponse(
            data={"preference": update_user_preference_entity.to_dict()},
            message="preference update success",
        ).json()

    return ApiResponse(
        HttpRequstEnum.METHOD_NOT_ALLOWED.value, message="method not allowed"
    ).json()


# Api for community module.


# Api for popular module.


# Api for post module.


# Api for search module.


# Api for notice module.


# Api for others.


@api_bp.route("/categories", methods=["GET"])
@login_required
def categories() -> ApiResponse:
    """Get all categories."""

    category_entities = Category.query.all()
    category_collection = [category.to_dict() for category in category_entities]

    return ApiResponse(data={"categories": category_collection}).json()


@api_bp.route("/categories/<category_id>", methods=["GET"])
@login_required
def category(category_id: int) -> ApiResponse:
    """Get a category by id."""

    category_entity = Category.query.get(category_id)

    if category_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="category not found"
        ).json()

    return ApiResponse(data={"category": category_entity.to_dict()}).json()


@api_bp.route("/tags", methods=["GET"])
@login_required
def tags() -> ApiResponse:
    """Get all tags."""

    tag_entities = Tag.query.all()
    tags_collection = [tag.to_dict() for tag in tag_entities]

    return ApiResponse(data={"tags": tags_collection}).json()


@api_bp.route("/tags/<tag_id>", methods=["GET"])
@login_required
def tag(tag_id: int) -> ApiResponse:
    """Get a tag by id."""

    tag_entity = Tag.query.get(tag_id)

    if tag_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="tag not found"
        ).json()

    return ApiResponse(data={"tag": tag_entity.to_dict()}).json()
