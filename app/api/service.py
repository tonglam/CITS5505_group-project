"""Services for api."""

import requests
from flask import current_app, g
from flask_login import current_user
from werkzeug.datastructures import FileStorage

from app.constants import IMAGE_BB_UPLOAD_URL, HttpRequestEnum
from app.extensions import db
from app.models.category import Category
from app.models.community import Community
from app.models.reply import Reply
from app.models.request import Request
from app.models.tag import Tag
from app.models.trending import Trending
from app.models.user import User
from app.models.user_like import UserLike
from app.models.user_notice import UserNotice
from app.models.user_preference import UserPreference
from app.models.user_record import UserRecord
from app.models.user_save import UserSave
from app.notice.events import NoticeTypeEnum, notice_event
from app.utils import get_config

from . import ApiResponse

# Api service for auth module.


def user_verification_service(user_name: str) -> ApiResponse:
    """verify the user's identity."""

    result_count = User.query.filter_by(username=user_name).count()

    return (
        ApiResponse(data={"result": False}).json()
        if result_count
        else ApiResponse(data={"result": True}).json()
    )


def user_email_verify_service(user_email: str) -> ApiResponse:
    """verify the user's identity."""

    result_count = User.query.filter_by(email=user_email).count()

    return (
        ApiResponse(data={"result": False}).json()
        if result_count
        else ApiResponse(data={"result": True}).json()
    )


def user_password_verify_service(user_password: str) -> ApiResponse:
    """verify the user's password."""

    result_count = User.query.filter_by(password_hash=user_password).count()

    return (
        ApiResponse(data={"result": False}).json()
        if result_count
        else ApiResponse(data={"result": True}).json()
    )


# Api service for user module.


def user_communities_service(page: int = 1, per_page: int = 10) -> ApiResponse:
    """Service for getting all user communities."""

    user_id: str = current_user.id

    # basic query
    user_communities = (
        db.session.query(UserPreference).filter_by(user_id=user_id).first()
    )
    community_ids = _get_user_community_ids(user_communities)

    # retrieve communities
    query = db.session.query(Community).filter(Community.id.in_(community_ids))

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    community_collection = [community.to_dict() for community in pagination.items]

    return ApiResponse(
        data={"user_communities": community_collection}, pagination=pagination
    ).json()


def user_posts_service(page: int = 1, per_page: int = 10) -> ApiResponse:
    """Service for getting all user posts."""

    user_id: str = current_user.id

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


def user_replies_service(page: int = 1, per_page: int = 10) -> ApiResponse:
    """Service for getting all user replies."""

    user_id: str = current_user.id

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


def users_records_service(
    page: int = 1,
    per_page: int = 10,
) -> ApiResponse:
    """Service for getting all users records."""

    user_id: str = current_user.id

    # basic query
    query = (
        db.session.query(UserRecord)
        .filter_by(user_id=user_id)
        .order_by(UserRecord.create_at.desc())
    )

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    user_record_collection = [record.to_dict() for record in pagination.items]

    return ApiResponse(
        data={"user_records": user_record_collection}, pagination=pagination
    ).json()


def post_user_record_service(request_id: int) -> ApiResponse:
    """Service for posting a user view record by record id."""

    # validate request_id
    request_entity = db.session.query(Request).get(request_id)
    if request_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="request not found"
        ).json()

    user_id: str = current_user.id

    # check if user record already exists
    user_record_entity = (
        db.session.query(UserRecord)
        .filter_by(user_id=user_id, request_id=request_id)
        .first()
    )

    if user_record_entity is not None:
        return ApiResponse(
            HttpRequestEnum.BAD_REQUEST.value, message="user record already exists"
        ).json()

    # add user record
    user_record_entity = UserRecord(user_id=user_id, request_id=request_id)
    db.session.add(user_record_entity)
    db.session.commit()
    current_app.logger.info(
        f"User {user_id} added Record for Request {request_id} successfully"
    )

    return ApiResponse(
        HttpRequestEnum.CREATED.value, message="add user record success"
    ).json()


def delete_user_record_service(request_id: int) -> ApiResponse:
    """Service for deleting a user view record by record id."""

    # validate request_id
    request_entity = db.session.query(Request).get(request_id)
    if request_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="request not found"
        ).json()

    user_id: str = current_user.id

    # check if user record already exists
    user_record_entity = (
        db.session.query(UserRecord)
        .filter_by(user_id=user_id, request_id=request_id)
        .first()
    )

    if user_record_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="user record not found"
        ).json()

    # delete request record
    db.session.delete(user_record_entity)
    db.session.commit()

    current_app.logger.info(
        f"User {user_id} removed Record for Request {request_id} successfully"
    )

    return ApiResponse(
        HttpRequestEnum.NO_CONTENT.value, message="delete user record success"
    ).json()


def user_likes_service(page: int = 1, per_page: int = 10) -> ApiResponse:
    """Service for getting all user likes."""

    user_id: str = current_user.id

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


def post_user_like_service(request_id: int) -> ApiResponse:
    """Service for liking a request of a reply."""

    # validate request_id
    request_entity = db.session.query(Request).get(request_id)
    if request_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="request not found"
        ).json()

    user_id: str = current_user.id

    # check if user like already exists
    user_like_entity = (
        db.session.query(UserLike)
        .filter_by(user_id=user_id, request_id=request_id)
        .first()
    )

    if user_like_entity is not None:
        return ApiResponse(
            HttpRequestEnum.BAD_REQUEST.value, message="like already exists"
        ).json()

    # add user like
    user_like_entity = UserLike(user_id=user_id, request_id=request_id)
    db.session.add(user_like_entity)
    db.session.commit()
    current_app.logger.info(f"User {user_id} liked Request {request_id} successfully")

    return ApiResponse(HttpRequestEnum.CREATED.value, message="like success").json()


def delete_user_like_service(request_id: int) -> ApiResponse:
    """Service for unliking a request of a reply."""

    # validate request_id
    request_entity = db.session.query(Request).get(request_id)
    if request_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="request not found"
        ).json()

    user_id: str = current_user.id

    # check if user like exists
    user_like_entity = (
        db.session.query(UserLike)
        .filter_by(user_id=user_id, request_id=request_id)
        .first()
    )

    if user_like_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="like not found"
        ).json()

    # unlike request
    db.session.delete(user_like_entity)
    db.session.commit()

    current_app.logger.info(f"User {user_id} unliked Request {request_id} successfully")

    return ApiResponse(
        HttpRequestEnum.NO_CONTENT.value, message="unlike success"
    ).json()


def user_saves_service(page: int = 1, per_page: int = 10) -> ApiResponse:
    """Service for getting all user saves."""

    user_id: str = current_user.id

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
        HttpRequestEnum.CREATED.value,
        data={"user_saves": save_collection},
        pagination=pagination,
    ).json()


def post_user_save_service(request_id: int) -> ApiResponse:
    """Service for saving a post of a reply."""

    # validate request_id
    request_entity = db.session.query(Request).get(request_id)
    if request_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="request not found"
        ).json()

    user_id: str = current_user.id

    # check if user save already exists
    user_save_entity = (
        db.session.query(UserSave)
        .filter_by(user_id=user_id, request_id=request_id)
        .first()
    )

    if user_save_entity is not None:
        return ApiResponse(
            HttpRequestEnum.BAD_REQUEST.value, message="save already exists"
        ).json()

    # add user save
    user_save_entity = UserSave(user_id=user_id, request_id=request_id)
    db.session.add(user_save_entity)
    db.session.commit()
    current_app.logger.info(f"User {user_id} saved Request {request_id} successfully")

    return ApiResponse(HttpRequestEnum.CREATED.value, message="save success").json()


def delete_user_save_service(request_id: int) -> ApiResponse:
    """Service for deleting a user save of a reply."""

    # validate request_id
    request_entity = db.session.query(Request).get(request_id)
    if request_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="request not found"
        ).json()

    user_id: str = current_user.id

    # check if user save exists
    user_save_entity = (
        db.session.query(UserSave)
        .filter_by(user_id=user_id, request_id=request_id)
        .first()
    )

    if user_save_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="save not found"
        ).json()

    # unsave request
    db.session.delete(user_save_entity)
    db.session.commit()

    current_app.logger.info(f"User {user_id} unsaved Request {request_id} successfully")

    return ApiResponse(
        HttpRequestEnum.NO_CONTENT.value, message="unsave success"
    ).json()


def users_notices_service(
    notice_type: str = None,
    status: str = None,
    order_by: str = "create_at_desc",
    page: int = 1,
    per_page: int = 5,
) -> ApiResponse:
    """Service for getting all users notices."""

    user_id: str = current_user.id

    # basic query
    query = (
        db.session.query(UserNotice)
        .filter_by(user_id=user_id)
        .order_by(UserNotice.status)
        .order_by(UserNotice.create_at.desc())
    )

    # apply filters
    if notice_type:
        query = query.filter(UserNotice.module == notice_type)
    if status:
        status = 1 if status == "read" else 0
        query = query.filter(UserNotice.status == status)

    # apply sort
    if order_by == "create_at":
        query = query.order_by(UserNotice.create_at)
    elif order_by == "create_at_desc":
        query = query.order_by(UserNotice.create_at.desc())
    elif order_by == "status":
        query = query.order_by(UserNotice.status)

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    notice_collection = [notice.to_dict() for notice in pagination.items]

    return ApiResponse(
        data={"user_notices": notice_collection}, pagination=pagination
    ).json()


def get_user_notice_service(notice_id: int) -> ApiResponse:
    """Service for getting a user notice by notice id."""

    notice_entity = db.session.query(UserNotice).get(notice_id)

    if notice_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="user notice not found"
        ).json()

    return ApiResponse(data={"user_notice": notice_entity.to_dict()}).json()


def put_user_notice_service(notice_id: int) -> ApiResponse:
    """Service for updating a user notice by notice id."""

    notice_entity = db.session.query(UserNotice).get(notice_id)

    if notice_entity is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="user notice not found"
        ).json()

    # update notice status
    notice_entity.status = not notice_entity.status
    db.session.commit()

    # update global notice number
    g.notice_num = db.session.query(UserNotice).filter_by(status=0).count()

    return ApiResponse(
        HttpRequestEnum.NO_CONTENT.value,
        message="update success",
    ).json()


def user_stats_service() -> ApiResponse:
    """Service for getting user stats."""

    if current_user.is_anonymous:
        return ApiResponse(data={"user_stats": None}).json()

    user_id = current_user.id

    user_preference = (
        db.session.query(UserPreference).filter_by(user_id=user_id).first()
    )
    community_ids = _get_user_community_ids(user_preference)

    community_num = len(community_ids)
    request_num = db.session.query(Request).filter_by(author_id=user_id).count()
    reply_num = db.session.query(Reply).filter_by(replier_id=user_id).count()
    view_num = db.session.query(UserRecord).filter_by(user_id=user_id).count()
    like_num = db.session.query(UserLike).filter_by(user_id=user_id).count()
    save_num = db.session.query(UserSave).filter_by(user_id=user_id).count()

    stats = {
        "community_num": community_num,
        "request_num": request_num,
        "view_num": view_num,
        "reply_num": reply_num,
        "like_num": like_num,
        "save_num": save_num,
    }

    return ApiResponse(data={"user_stats": stats}).json()


def _get_user_community_ids(user_preference: UserPreference) -> list:
    """Get user community ids from user preference."""

    if user_preference is None:
        return []

    if user_preference.communities is None or user_preference.communities == "":
        return []

    return [
        int(id.strip()) for id in user_preference.communities.strip("[]").split(",")
    ]


# Api service for community module.


def communities_service(page: int = 1, per_page: int = 10) -> ApiResponse:
    """Service for getting all communities."""

    # query
    query = db.session.query(Community).order_by(Community.id)

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    community_collection = [community.to_dict() for community in pagination.items]

    # community posts number
    for community in community_collection:
        community["posts"] = (
            db.session.query(Request).filter_by(community_id=community["id"]).count()
        )

    # if user joined community
    user_communities = (
        db.session.query(UserPreference).filter_by(user_id=current_user.id).first()
    )
    community_ids = _get_user_community_ids(user_communities)

    for community in community_collection:
        community["joined"] = community["id"] in community_ids

    # community members number
    for community in community_collection:
        community["members"] = (
            db.session.query(User)
            .join(User.communities)
            .filter(Community.id == community["id"])
            .count()
        )

    return ApiResponse(
        data={"communities": community_collection}, pagination=pagination
    ).json()


def join_community_service(community_id: int) -> ApiResponse:
    """Service for joining a community by community id."""

    user_id: str = current_user.id

    # check if user already joined community
    community = db.session.query(Community).get(community_id)
    if community is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="community not found"
        ).json()

    user_preference = (
        db.session.query(UserPreference).filter_by(user_id=user_id).first()
    )

    if user_preference is None:
        user_preference = UserPreference(
            user_id=user_id, communities=str([community_id]), interests=str([])
        )
        db.session.add(user_preference)

    else:
        community_ids = _get_user_community_ids(user_preference)
        if community in community_ids:
            return ApiResponse(
                HttpRequestEnum.BAD_REQUEST.value,
                message="user already joined community",
            ).json()

        user_preference.communities = str(
            list(set(_get_user_community_ids(user_preference) + [community_id]))
        )

    db.session.commit()
    current_app.logger.info(
        f"User: {user_id} joined Community {community_id} successfully"
    )
    notice_event(notice_type=NoticeTypeEnum.COMMUNITY_JOIN)

    return ApiResponse(
        HttpRequestEnum.SUCCESS_OK.value, message="join community success"
    ).json()


def leave_community_service(community_id: int) -> ApiResponse:
    """Service for leaving a community by community id."""

    user_id: str = current_user.id

    # check if user already joined community
    community = db.session.query(Community).get(community_id)
    if community is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="community not found"
        ).json()

    user_preference = (
        db.session.query(UserPreference).filter_by(user_id=user_id).first()
    )

    if user_preference is None:
        return ApiResponse(
            HttpRequestEnum.BAD_REQUEST.value, message="user not joined community"
        ).json()

    community_ids = _get_user_community_ids(user_preference)
    if community_id not in community_ids:
        return ApiResponse(
            HttpRequestEnum.BAD_REQUEST.value, message="user not joined community"
        ).json()

    community_ids.remove(community_id)
    user_preference.communities = str(community_ids)
    db.session.commit()
    current_app.logger.info(
        f"User: {user_id} left Community {community_id} successfully"
    )
    notice_event(notice_type=NoticeTypeEnum.COMMUNITY_LEAVE)

    return ApiResponse(
        HttpRequestEnum.SUCCESS_OK.value, message="leave community success"
    ).json()


def delete_community_service(community_id: int) -> ApiResponse:
    """Service for deleting a community by community id."""

    user_id: str = current_user.id

    # check if user is admin of community
    community = db.session.query(Community).get(community_id)
    if community is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="community not found"
        ).json()

    if community.creator_id != user_id:
        return ApiResponse(
            HttpRequestEnum.FORBIDDEN.value, message="user is not creator of community"
        ).json()

    # delete community
    db.session.delete(community)
    db.session.commit()
    current_app.logger.info(f"User: {user_id} deleted Community {community_id}")
    notice_event(notice_type=NoticeTypeEnum.COMMUNITY_DELETED)

    return ApiResponse(
        HttpRequestEnum.NO_CONTENT.value, message="delete community success"
    ).json()


def community_options_service() -> ApiResponse:
    """Service for getting community options."""

    communities = db.session.query(Community).order_by(Community.id).all()
    community_options = [
        {"value": community.id, "label": community.name} for community in communities
    ]

    return ApiResponse(data={"community_options": community_options}).json()


# Api service for popular module.


def populars_service(limit: int = 10) -> ApiResponse:
    """Get all popular requests by limit."""

    # query
    trendings = (
        db.session.query(Trending).order_by(Trending.view_num.desc()).limit(limit)
    )

    # convert to JSON data
    popular_collection = [trending.to_dict() for trending in trendings]

    return ApiResponse(data={"populars": popular_collection}).json()


# Api service for post module.


def posts_service(
    community_id: int,
    order_by: str = "create_at_desc",
    page: int = 1,
    per_page: int = 10,
) -> ApiResponse:
    """Service for getting all posts."""

    # basic query
    query = db.session.query(Request)

    # apply filters
    if community_id:
        query = query.filter(Request.community_id == community_id)

    # apply sort
    if order_by == "create_at_desc":
        query = query.order_by(Request.create_at.desc())
    elif order_by == "update_at_desc":
        query = query.order_by(Request.update_at.desc())
    elif order_by == "reply_num_desc":
        query = query.order_by(Request.reply_num.desc())
    elif order_by == "view_num_desc":
        query = query.order_by(Request.view_num.desc())
    elif order_by == "like_num_desc":
        query = query.order_by(Request.like_num.desc())
    elif order_by == "save_num_desc":
        query = query.order_by(Request.save_num.desc())

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    post_collection = [post.to_dict() for post in pagination.items]

    return ApiResponse(data={"posts": post_collection}, pagination=pagination).json()


# Api service for notice module.


# Api service for others.


def categories_service() -> ApiResponse:
    """Service for getting all categories."""

    # query
    categories = db.session.query(Category).order_by(Category.id)

    # convert to JSON data
    category_collection = [category.to_dict() for category in categories]

    return ApiResponse(data={"categories": category_collection}).json()


def category_service(category_id: int) -> ApiResponse:
    """Service for getting a category."""

    category = Category.query.get(category_id)

    if category is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="category not found"
        ).json()

    return ApiResponse(data={"category": category.to_dict()}).json()


def tags_service() -> ApiResponse:
    """Service for getting all tags."""

    # query
    tags = db.session.query(Tag).order_by(Tag.id)

    # convert to JSON data
    tags_collection = [tag.to_dict() for tag in tags]

    return ApiResponse(data={"tags": tags_collection}).json()


def tag_service(tag_id: int) -> ApiResponse:
    """Service for getting a tag."""

    tag = Tag.query.get(tag_id)

    if tag is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="tag not found"
        ).json()

    return ApiResponse(data={"tag": tag.to_dict()}).json()


def stats_service() -> ApiResponse:
    """Service for getting stats."""

    user_num = db.session.query(User).count()
    community_num = db.session.query(Community).count()
    request_num = db.session.query(Request).count()
    reply_num = db.session.query(Reply).count()
    view_num = db.session.query(UserRecord).count()
    like_num = db.session.query(UserLike).count()
    save_num = db.session.query(UserSave).count()

    stats = {
        "user_num": user_num,
        "community_num": community_num,
        "request_num": request_num,
        "view_num": view_num,
        "reply_num": reply_num,
        "like_num": like_num,
        "save_num": save_num,
    }

    return ApiResponse(data={"stats": stats}).json()


def upload_image_service(image_file: FileStorage) -> ApiResponse:
    """Service for uploading image."""

    if image_file is None:
        return ApiResponse(
            code=HttpRequestEnum.BAD_REQUEST.value,
            message="Image file is required",
        ).json()

    payload = payload = {"key": get_config("IMGBB", "API_KEY")}
    files = {
        "image": (image_file.filename, image_file, image_file.content_type),
    }

    response = requests.post(IMAGE_BB_UPLOAD_URL, data=payload, files=files, timeout=10)
    current_app.logger.info(f"Image BB upload response: {response}")

    if response.status_code != 200:
        return ApiResponse(
            code=HttpRequestEnum.INTERNAL_SERVER_ERROR.value,
            message="Image upload failed",
        ).json()

    image_url = response.json()["data"]["url"]

    return ApiResponse(
        data={"image_url": image_url}, message="Image uploaded successfully"
    ).json()
