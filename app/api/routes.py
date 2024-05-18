"""Routes for api."""
from urllib.parse import urlparse, parse_qs

import requests
from flask import abort, request
from flask_jwt_extended import jwt_required

from app.api import api_bp
from app.constants import IMAGE_BB_UPLOAD_URL, HttpRequestEnum
from app.utils import get_config

from . import ApiResponse
from .service import (
    categories_service,
    category_service,
    delete_community_service,
    delete_user_like_service,
    delete_user_record_service,
    delete_user_save_service,
    get_user_notice_service,
    join_community_service,
    leave_community_service,
    post_user_like_service,
    post_user_record_service,
    post_user_save_service,
    posts_service,
    put_user_notice_service,
    stats_service,
    tag_service,
    tags_service,
    user_communities_service,
    user_email_verify_service,
    user_likes_service,
    user_password_verify_service,
    user_posts_service,
    user_replies_service,
    user_saves_service,
    user_stats_service,
    user_verification_service,
    users_notices_service,
    users_records_service,
    post_user_comments_service,
    delete_user_comments_service,
    update_user_comments_service,
    user_post_service,
    delete_post_service,
    update_user_post_service,
)


# Api for auth module.
@api_bp.route("/users/username/<user_name>", methods=["GET"])
@jwt_required()
def user_verification(user_name: str) -> ApiResponse:
    """verify the user's identity."""

    return user_verification_service(user_name)


@api_bp.route("/users/email/<user_email>", methods=["GET"])
@jwt_required()
def user_verification_email(user_email: str) -> ApiResponse:
    """verify the user's email."""

    return user_email_verify_service(user_email)


@api_bp.route("/users/email/<user_password>", methods=["GET"])
@jwt_required()
def user_verification_password(user_password: str) -> ApiResponse:
    """verify the user's password."""

    return user_password_verify_service(user_password)


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


@api_bp.route("/users/likes", methods=["POST", "DELETE"])
@jwt_required()
def user_like() -> ApiResponse:
    """Like or unlike a request by user id and request id."""
    request_id = request.get_json().get("request_id")
    reply_id = request.get_json().get("reply_id")

    if request.method == "POST":
        return post_user_like_service(request_id, reply_id)

    if request.method == "DELETE":
        return delete_user_like_service(request_id, reply_id)

    abort(HttpRequestEnum.METHOD_NOT_ALLOWED.value)


@api_bp.route("/users/saves", methods=["GET"])
@jwt_required()
def user_saves() -> ApiResponse:
    """Get all saves by user id."""

    # pagination parameters
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    return user_saves_service(page, per_page)


@api_bp.route("/users/saves", methods=["POST", "DELETE"])
@jwt_required()
def user_save() -> ApiResponse:
    """Save or unsave a request or a reply by user id and request id."""
    request_id = request.get_json().get("request_id")
    reply_id = request.get_json().get("reply_id")

    if request.method == "POST":
        return post_user_save_service(request_id, reply_id)

    if request.method == "DELETE":
        return delete_user_save_service(request_id, reply_id)

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


@api_bp.route("/users/stats", methods=["GET"])
def user_stats():
    """Get the user's statistics."""

    return user_stats_service()


# Api for community module.


@api_bp.route("/communities/<int:community_id>/join", methods=["POST"])
@jwt_required()
def join_community(community_id: int) -> ApiResponse:
    """Join a community by user id and community id."""

    return join_community_service(community_id)


@api_bp.route("/communities/<int:community_id>/leave", methods=["POST"])
@jwt_required()
def leave_community(community_id: int) -> ApiResponse:
    """Leave a community by user id and community id."""

    return leave_community_service(community_id)


@api_bp.route("/communities/<int:community_id>/delete", methods=["DELETE"])
@jwt_required()
def delete_community(community_id: int) -> ApiResponse:
    """Delete a community by id."""

    return delete_community_service(community_id)


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

@api_bp.route("/posts/create/comment", methods=["POST","PUT","DELETE"])
@jwt_required()
def post_comment() -> ApiResponse:
    """Post, update and delete comment."""
    # Get the information from the referer header.
    referer = request.headers.get('Referer')
    if referer:
        query = urlparse(referer).query
        params = parse_qs(query)
        post_id = params.get('post_id', [None])[0]
        reply_id = params.get('reply_id', [post_id])[0]
    else:
        post_id = None
        reply_id = None

    content = request.json.get('content')

    request_post_id = request.json.get('post_id')
    request_reply_id = request.json.get('reply_id')

    if request.method == "POST":
        if not post_id or not content:
            return ApiResponse(400, 'Wrong parameters for post comment').json()
        return post_user_comments_service(post_id, reply_id, content)

    if request.method == "PUT":
        return update_user_comments_service(reply_id, content)

    if request.method == "DELETE":
        return delete_user_comments_service(request_post_id, request_reply_id)

    return ApiResponse(400, 'Invalid request method').json()

@api_bp.route("/posts/create/post", methods=["POST", "PUT", "DELETE"])
@jwt_required()
def post_related() -> ApiResponse:
    # pylint: disable=too-many-return-statements
    """Post, update, and delete a post."""

    title = request.json.get('title')
    community = request.json.get('community')
    content = request.json.get('content')
    tag_id = request.json.get('tag')
    request_post_id = request.json.get('post_id')

    referer = request.headers.get('Referer')
    if referer:
        query = urlparse(referer).query
        params = parse_qs(query)
        referer_post_id = params.get('post_id', [None])[0]
    else:
        referer_post_id = None

    if request.method == "POST":
        if not title or not community or not content:
            return ApiResponse(400, 'Wrong parameters for post').json()
        return user_post_service(title, community, content, tag_id)

    if request.method == "PUT":
        if not referer_post_id:
            return ApiResponse(400, 'Post ID missing for update').json()
        return update_user_post_service(referer_post_id, title, community, content, tag_id)

    if request.method == "DELETE":
        if not request_post_id:
            return ApiResponse(400, 'Post ID missing for deletion').json()
        return delete_post_service(request_post_id)

    return ApiResponse(400, 'Invalid request method').json()

# Api for others.


@api_bp.route("/categories", methods=["GET"])
@jwt_required()
def categories() -> ApiResponse:
    """Get all categories."""

    return categories_service()


@api_bp.route("/categories/<category_id>", methods=["GET"])
@jwt_required()
def category(category_id: int) -> ApiResponse:
    """Get a category by id."""

    return category_service(category_id)


@api_bp.route("/tags", methods=["GET"])
@jwt_required()
def tags() -> ApiResponse:
    """Get all tags."""

    return tags_service()


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


@api_bp.route("/upload/image", methods=["POST"])
@jwt_required()
def upload_image() -> ApiResponse:
    """Upload image to imgbb."""

    # image file
    image_file = request.files.get("image")

    # post image to imgbb
    payload = payload = {
        "key": get_config("IMG_BB", "API_KEY"),
        "image": image_file.read(),
    }

    # request
    response = requests.post(IMAGE_BB_UPLOAD_URL, files=payload, timeout=10)

    if response.status_code != 200:
        return ApiResponse(
            code=HttpRequestEnum.INTERNAL_SERVER_ERROR.value,
            message="Image upload failed",
        )

    image_url = response.json()["data"]["url"]

    return ApiResponse(
        data={"image_url": image_url}, message="Image uploaded successfully"
    )
