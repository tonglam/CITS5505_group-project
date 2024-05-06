"""Routes for api."""

from dataclasses import dataclass

from flask import abort, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from flask_login import current_user
from flask_sqlalchemy import pagination as Pagination

from app.api import api_bp
from app.constants import HttpRequstEnum
from app.extensions import db
from app.models.category import Category
from app.models.reply import Reply
from app.models.request import Request
from app.models.tag import Tag
from app.models.user import User
from app.models.user_like import UserLike
from app.models.user_notice import UserNotice
from app.models.user_preference import UserPreference
from app.models.user_record import UserRecord
from app.models.user_save import UserSave
from app.notice.events import NoticeTypeEnum, notice_event

from .service import update_user_data, update_user_preference_data


@dataclass
class ApiResponse:
    """Api response template data class."""

    code: HttpRequstEnum = HttpRequstEnum.SUCCESS_OK.value
    data: object = None
    message: str = "success"
    pagination: Pagination = None

    def json(self) -> str:
        """Convert the response to JSON."""

        response_dict = {
            "code": self.code,
            "data": self.data,
            "message": self.message,
        }

        if self.pagination:
            response_dict["pagination"] = {
                "page": self.pagination.page,
                "per_page": self.pagination.per_page,
                "total_items": self.pagination.total,
                "total_pages": self.pagination.pages,
            }

        return jsonify(response_dict)


# Api for auth module.


# Api for user module.


@api_bp.route("/users/<username>", methods=["GET", "PUT"])
@jwt_required()
def users(username: str) -> ApiResponse:
    """Retrieve or update a user by username."""

    user_entity = db.session.query(User).filter_by(username=username).first()

    if user_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="user not found"
        ).json()

    if request.method == "GET":
        return ApiResponse(data={"user": user_entity.to_dict()}).json()

    if request.method == "PUT":
        # check user permission, only login user can access their own data
        if current_user.id != user_entity.id:
            abort(HttpRequstEnum.FORBIDDEN.value)

        # TODO: validate request data, using a User WTForm

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
        current_app.logger.info(
            f"User {current_user.id} updated successfully: {update_user_entity}"
        )

        # send notification
        notice_event(notice_type=NoticeTypeEnum.USER_UPDATED_PROFILE)

        return ApiResponse(
            data={"user": update_user_entity.to_dict()}, message="user update success"
        ).json()

    abort(HttpRequstEnum.METHOD_NOT_ALLOWED.value)


@api_bp.route("/users/preference", methods=["GET", "PUT"])
@jwt_required()
def user_preference() -> ApiResponse:
    """Retrieve or update user preferences."""

    user_preference_entity = (
        db.session.query(UserPreference).filter_by(user_id=current_user.id).first()
    )
    if user_preference_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="user preference not found"
        ).json()

    if request.method == "GET":
        return ApiResponse(data={"preference": user_preference_entity.to_dict()}).json()

    if request.method == "PUT":
        # TODO: validate request data, using a UserPreference WTForm

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
        current_app.logger.info(
            f"User {current_user.id} preference \
                updated successfully: {update_user_preference_entity}"
        )

        return ApiResponse(
            data={"preference": update_user_preference_entity.to_dict()},
            message="preference update success",
        ).json()

    abort(HttpRequstEnum.METHOD_NOT_ALLOWED.value)


@api_bp.route("/users/records", methods=["GET"])
@jwt_required()
def user_records() -> ApiResponse:
    """Retrieve all records associated with the logged-in user."""

    user_id = current_user.id

    # get filter parameters
    request_id_filter = request.args.get("request_id")
    record_type_filter = request.args.get("record_type")

    # get sort parameters
    order_by = request.args.get("order_by")

    # get pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    # basic query
    query = db.session.query(UserRecord).filter_by(user_id=user_id)

    # apply filters
    if request_id_filter:
        query = query.filter(UserRecord.request_id == request_id_filter)

    if record_type_filter:
        query = query.filter(UserRecord.record_type == record_type_filter)

    # apply sort
    if order_by == "update_at":
        query = query.order_by(UserRecord.update_at)
    elif order_by == "update_at_desc":
        query = query.order_by(UserRecord.update_at.desc())

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    user_record_collection = [record.to_dict() for record in pagination.items]

    return ApiResponse(
        data={"user_records": user_record_collection}, pagination=pagination
    ).json()


@api_bp.route("/users/records/<int:record_id>", methods=["GET", "DELETE"])
@jwt_required()
def users_record(record_id: int) -> ApiResponse:
    """Retrieve or delete a specific user record by ID."""

    record_entity = (
        db.session.query(UserRecord)
        .filter_by(id=record_id, user_id=current_user.id)
        .first()
    )
    if record_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="record not found"
        ).json()

    if request.method == "GET":
        return ApiResponse(data={"record": record_entity.to_dict()}).json()

    if request.method == "DELETE":
        db.session.delete(record_entity)
        db.session.commit()
        current_app.logger.info(
            f"User {current_user.id}, Record {record_id} deleted successfully"
        )

        return ApiResponse(
            HttpRequstEnum.NO_CONTENT.value, message="record delete success"
        ).json()

    abort(HttpRequstEnum.METHOD_NOT_ALLOWED.value)


@api_bp.route("/users/posts", methods=["GET"])
@jwt_required()
def user_posts() -> ApiResponse:
    """Get all posts by user id."""

    user_id = current_user.id

    # pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    # basic query
    query = (
        db.session.query(Request)
        .filter_by(author_id=user_id)
        .order_by(Request.create_at.desc())
    )

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    post_collection = [post.to_dict() for post in pagination.items]

    return ApiResponse(
        data={"user_posts": post_collection}, pagination=pagination
    ).json()


@api_bp.route("/users/replies", methods=["GET"])
@jwt_required()
def user_replies() -> ApiResponse:
    """Get all replies by user id."""

    user_id = current_user.id

    # pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    # basic query
    query = (
        db.session.query(Reply)
        .filter_by(replier_id=user_id)
        .order_by(Reply.create_at.desc())
    )

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    reply_collection = [reply.to_dict() for reply in pagination.items]

    return ApiResponse(
        data={"user_replies": reply_collection}, pagination=pagination
    ).json()


@api_bp.route("/users/likes", methods=["GET"])
@jwt_required()
def user_likes() -> ApiResponse:
    """Get all likes by user id."""

    user_id = current_user.id

    # pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    # basic query
    query = (
        db.session.query(UserLike)
        .filter_by(user_id=user_id)
        .order_by(UserLike.create_at.desc())
    )

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    like_collection = [like.to_dict() for like in pagination.items]

    return ApiResponse(
        data={"user_likes": like_collection}, pagination=pagination
    ).json()


@api_bp.route("/users/likes/<int:request_id>", methods=["POST", "DELETE"])
@jwt_required()
def user_like(request_id: int) -> ApiResponse:
    """Like or unlike a request by user id and request id."""

    user_id = current_user.id

    like_entity = (
        db.session.query(UserLike)
        .filter_by(user_id=user_id, request_id=request_id)
        .first()
    )

    if request.method == "POST":
        # validate request_id
        request_entity = db.session.query(Request).get(request_id)
        if request_entity is None:
            return ApiResponse(
                HttpRequstEnum.NOT_FOUND.value, message="request not found"
            ).json()

        if like_entity is not None:
            return ApiResponse(
                HttpRequstEnum.BAD_REQUEST.value, message="like already exists"
            ).json()

        # add user like
        like_entity = UserLike(user_id=user_id, request_id=request_id)
        db.session.add(like_entity)
        db.session.commit()
        current_app.logger.info(
            f"User {user_id} liked Request {request_id} successfully"
        )

        return ApiResponse(
            HttpRequstEnum.CREATED.value,
            message="like success",
        ).json()

    if request.method == "DELETE":
        if like_entity is None:
            return ApiResponse(
                HttpRequstEnum.NOT_FOUND.value, message="like not found"
            ).json()

        # unlike request
        db.session.delete(like_entity)
        db.session.commit()
        current_app.logger.info(
            f"User {user_id} unliked Request {request_id} successfully"
        )

        return ApiResponse(
            HttpRequstEnum.NO_CONTENT.value, message="unlike success"
        ).json()

    abort(HttpRequstEnum.METHOD_NOT_ALLOWED.value)


@api_bp.route("/users/saves", methods=["GET"])
@jwt_required()
def user_saves() -> ApiResponse:
    """Get all saves by user id."""

    user_id = current_user.id

    # pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    # basic query
    query = (
        db.session.query(UserSave)
        .filter_by(user_id=user_id)
        .order_by(UserSave.create_at.desc())
    )

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    save_collection = [save.to_dict() for save in pagination.items]

    return ApiResponse(
        HttpRequstEnum.CREATED.value,
        data={"user_saves": save_collection},
        pagination=pagination,
    ).json()


@api_bp.route("/users/saves/<int:request_id>", methods=["POST", "DELETE"])
@jwt_required()
def user_save(request_id: int) -> ApiResponse:
    """Save or unsave a request by user id and request id."""

    user_id = current_user.id

    save_entity = (
        db.session.query(UserSave)
        .filter_by(user_id=user_id, request_id=request_id)
        .first()
    )

    if request.method == "POST":
        # validate request_id
        request_entity = db.session.query(Request).get(request_id)
        if request_entity is None:
            return ApiResponse(
                HttpRequstEnum.NOT_FOUND.value, message="request not found"
            ).json()

        if save_entity is not None:
            return ApiResponse(
                HttpRequstEnum.BAD_REQUEST.value, message="save already exists"
            ).json()

        # add user save
        save_entity = UserSave(user_id=user_id, request_id=request_id)
        db.session.add(save_entity)
        db.session.commit()
        current_app.logger.info(
            f"User {user_id} saved Request {request_id} successfully"
        )

        return ApiResponse(HttpRequstEnum.CREATED.value, message="save success").json()

    if request.method == "DELETE":
        if save_entity is None:
            return ApiResponse(
                HttpRequstEnum.NOT_FOUND.value, message="save not found"
            ).json()

        # unsave request
        db.session.delete(save_entity)
        db.session.commit()
        current_app.logger.info(
            f"User {user_id} unsaved Request {request_id} successfully"
        )

        return ApiResponse(
            HttpRequstEnum.NO_CONTENT.value, message="unsave success"
        ).json()

    abort(HttpRequstEnum.METHOD_NOT_ALLOWED.value)


@api_bp.route("/users/notifications", methods=["GET"])
@jwt_required()
def user_notifications() -> ApiResponse:
    """Get all notifications by user id."""

    user_id = current_user.id

    # get filter parameters
    notice_type_filter = request.args.get("notice_type")
    status_filter = request.args.get("status")

    # get sort parameters
    order_by = request.args.get("order_by")

    # get pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    # basic query
    query = (
        db.session.query(UserNotice)
        .filter_by(user_id=user_id)
        .order_by(UserNotice.id)
        .order_by(UserNotice.status)
    )

    # apply filters
    if notice_type_filter:
        query = query.filter(UserNotice.module == notice_type_filter)
    if status_filter:
        status = 1 if status_filter == "read" else 0
        query = query.filter(UserNotice.status == status)

    # apply sort
    if order_by == "update_at":
        query = query.order_by(UserNotice.update_at)
    elif order_by == "update_at_desc":
        query = query.order_by(UserNotice.update_at.desc())
    elif order_by == "status":
        query = query.order_by(UserNotice.status)

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    notice_collection = [notice.to_dict() for notice in pagination.items]

    return ApiResponse(
        data={"user_notices": notice_collection}, pagination=pagination
    ).json()


@api_bp.route("/users/notifications/<int:notice_id>", methods=["GET", "PUT"])
@jwt_required()
def user_notice(notice_id: int) -> ApiResponse:
    """GET or PUT a notice by id."""

    notice_entity = db.session.query(UserNotice).get(notice_id)

    if notice_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="user notice not found"
        ).json()

    if request.method == "GET":
        return ApiResponse(data={"user_notice": notice_entity.to_dict()}).json()

    if request.method == "PUT":

        request_data = request.json

        if request_data is None or request_data == {} or "status" not in request_data:
            return ApiResponse(
                HttpRequstEnum.BAD_REQUEST.value,
                message="request data is empty, or missing status field",
            ).json()

        # update notice status
        notice_entity.status = request_data["status"]

        # update notice into database
        db.session.commit()

        return ApiResponse(
            data={"user_notice": notice_entity.to_dict()},
            message="user_notice status update success",
        ).json()

    abort(HttpRequstEnum.METHOD_NOT_ALLOWED.value)


# Api for community module.


# Api for popular module.


# Api for post module.


# Api for search module.

# Api for others.


@api_bp.route("/categories", methods=["GET"])
@jwt_required()
def categories() -> ApiResponse:
    """Get all categories."""

    # get pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    # query
    query = db.session.query(Category).order_by(Category.id)

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    category_collection = [category.to_dict() for category in pagination]

    return ApiResponse(
        data={"categories": category_collection}, pagination=pagination
    ).json()


@api_bp.route("/categories/<category_id>", methods=["GET"])
@jwt_required()
def category(category_id: int) -> ApiResponse:
    """Get a category by id."""

    category_entity = db.session.query(Category).get(category_id)

    if category_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="category not found"
        ).json()

    return ApiResponse(data={"category": category_entity.to_dict()}).json()


@api_bp.route("/tags", methods=["GET"])
@jwt_required()
def tags() -> ApiResponse:
    """Get all tags."""

    # get pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    # query
    query = db.session.query(Tag).order_by(Tag.id)

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    tags_collection = [tag.to_dict() for tag in pagination.items]

    return ApiResponse(data={"tags": tags_collection}, pagination=pagination).json()


@api_bp.route("/tags/<tag_id>", methods=["GET"])
@jwt_required()
def tag(tag_id: int) -> ApiResponse:
    """Get a tag by id."""

    tag_entity = db.session.query(Tag).get(tag_id)

    if tag_entity is None:
        return ApiResponse(
            HttpRequstEnum.NOT_FOUND.value, message="tag not found"
        ).json()

    return ApiResponse(data={"tag": tag_entity.to_dict()}).json()
