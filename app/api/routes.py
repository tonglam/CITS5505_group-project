"""Routes for api."""

from flask import abort, request
from flask_jwt_extended import jwt_required

from app.api import api_bp
from app.constants import HttpRequestEnum

from . import ApiResponse
from .service import (
    categories_service,
    category_service,
    delete_user_like_service,
    delete_user_record_service,
    delete_user_save_service,
    get_user_notice_service,
    post_user_like_service,
    post_user_record_service,
    post_user_save_service,
    posts_service,
    put_user_notice_service,
    stats_service,
    tag_service,
    tags_service,
    user_communities_service,
    user_likes_service,
    user_posts_service,
    user_replies_service,
    user_saves_service,
    users_notices_service,
    users_records_service,
)

# Api for auth module.


# Api for user module.


@api_bp.route("/users/communities", methods=["GET"])
@jwt_required()
def user_communities() -> ApiResponse:
    """Get all communities by user id."""

    # pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return user_communities_service(page, per_page)


@api_bp.route("/users/posts", methods=["GET"])
@jwt_required()
def user_posts() -> ApiResponse:
    """Get all posts by user id."""

    # pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return user_posts_service(page, per_page)


@api_bp.route("/users/replies", methods=["GET"])
@jwt_required()
def user_replies() -> ApiResponse:
    """Get all replies by user id."""

    # pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return user_replies_service(page, per_page)


@api_bp.route("/users/records", methods=["GET"])
# @jwt_required()
def user_records() -> ApiResponse:
    """Retrieve all records associated with the logged-in user."""

    # get pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return users_records_service(page, per_page)


@api_bp.route("/users/records/<int:request_id>", methods=["POST", "DELETE"])
@jwt_required()
def users_record(request_id: int) -> ApiResponse:
    """Save or delete a request view record by user id and request id."""

    if request.method == "POST":
        return post_user_record_service(request_id)

    if request.method == "DELETE":
        return delete_user_record_service(request_id)

    abort(HttpRequestEnum.METHOD_NOT_ALLOWED.value)


@api_bp.route("/users/likes", methods=["GET"])
# @jwt_required()
def user_likes() -> ApiResponse:
    """Get all likes by user id."""

    # pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return user_likes_service(page, per_page)


@api_bp.route("/users/likes/<int:request_id>", methods=["POST", "DELETE"])
@jwt_required()
def user_like(request_id: int) -> ApiResponse:
    """Like or unlike a request by user id and request id."""

    if request.method == "POST":
        return post_user_like_service(request_id)

    if request.method == "DELETE":
        return delete_user_like_service(request_id)

    abort(HttpRequestEnum.METHOD_NOT_ALLOWED.value)


@api_bp.route("/users/saves", methods=["GET"])
# @jwt_required()
def user_saves() -> ApiResponse:
    """Get all saves by user id."""

    # pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return user_saves_service(page, per_page)


@api_bp.route("/users/saves/<int:request_id>", methods=["POST", "DELETE"])
@jwt_required()
def user_save(request_id: int) -> ApiResponse:
    """Save or unsave a request by user id and request id."""

    if request.method == "POST":
        return post_user_save_service(request_id)

    if request.method == "DELETE":
        return delete_user_save_service(request_id)

    abort(HttpRequestEnum.METHOD_NOT_ALLOWED.value)


@api_bp.route("/users/notifications", methods=["GET"])
@jwt_required()
def user_notifications() -> ApiResponse:
    """Get all notifications by user id."""

    # get filter parameters
    notice_type = request.args.get("notice_type")
    status = request.args.get("status")

    # get sort parameters
    order_by = request.args.get("order_by")

    # get pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return users_notices_service(notice_type, status, order_by, page, per_page)


@api_bp.route("/users/notifications/<int:notice_id>", methods=["GET", "PUT"])
@jwt_required()
def user_notice(notice_id: int) -> ApiResponse:
    """GET or PUT a notice by id."""

    if request.method == "GET":
        return get_user_notice_service(notice_id)

    if request.method == "PUT":
        return put_user_notice_service(notice_id)

    abort(HttpRequestEnum.METHOD_NOT_ALLOWED.value)


# Api for community module.


# Api for popular module.


# Api for post module.


@api_bp.route("/posts", methods=["GET"])
@jwt_required()
def posts() -> ApiResponse:
    """Get all posts."""

    # get filter parameters
    community_id = request.args.get("community_id")

    # get sort parameters
    order_by = request.args.get("order_by")

    # get pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return posts_service(community_id, order_by, page, per_page)


# Api for others.


@api_bp.route("/categories", methods=["GET"])
@jwt_required()
def categories() -> ApiResponse:
    """Get all categories."""

    # get pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return categories_service(page=page, per_page=per_page)


@api_bp.route("/categories/<category_id>", methods=["GET"])
@jwt_required()
def category(category_id: int) -> ApiResponse:
    """Get a category by id."""

    return category_service(category_id)


@api_bp.route("/tags", methods=["GET"])
@jwt_required()
def tags() -> ApiResponse:
    """Get all tags."""

    # get pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return tags_service(page=page, per_page=per_page)


@api_bp.route("/tags/<tag_id>", methods=["GET"])
@jwt_required()
def tag(tag_id: int) -> ApiResponse:
    """Get a tag by id."""

    return tag_service(tag_id)


@api_bp.route("/stats", methods=["GET"])
@jwt_required()
def stats() -> ApiResponse:
    """Get all stats."""

    return stats_service()
