"""Services for api."""

from flask import current_app
from flask_login import current_user

from app.constants import HttpRequestEnum
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

from . import ApiResponse

# Api service for auth module.


# Api service for user module.


def user_communities_service(page: int = 1, per_page: int = 10) -> ApiResponse:
    """Service for getting all user communities."""

    user_id: str = current_user.id

    # basic query
    user_communities = (
        db.session.query(UserPreference).filter_by(user_id=user_id).first()
    )
    community_ids = [
        int(id.strip()) for id in user_communities.communities.strip("[]").split(",")
    ]

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
    order_by: str = "update_at_desc",
    page: int = 1,
    per_page: int = 10,
) -> ApiResponse:
    """Service for getting all users notices."""

    user_id: str = current_user.id

    # basic query
    query = (
        db.session.query(UserNotice)
        .filter_by(user_id=user_id)
        .order_by(UserNotice.id)
        .order_by(UserNotice.status)
    )

    # apply filters
    if notice_type:
        query = query.filter(UserNotice.module == notice_type)
    if status:
        status = 1 if status == "read" else 0
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

    return ApiResponse(
        HttpRequestEnum.NO_CONTENT.value,
        message="update success",
    ).json()


def user_stats_service() -> ApiResponse:
    """Service for getting user stats."""

    user_id = current_user.id

    user_preference = (
        db.session.query(UserPreference).filter_by(user_id=user_id).first()
    )
    community_ids = [
        int(id.strip()) for id in user_preference.communities.strip("[]").split(",")
    ]

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


# Api service for community module.


def communities_service() -> ApiResponse:
    """Service for getting all communities."""

    # query
    query = db.session.query(Community).order_by(Community.id)

    # convert to JSON data
    community_collection = [community.to_dict() for community in query]

    return ApiResponse(data={"communities": community_collection}).json()


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


def categories_service(page: int = 1, per_page: int = 10) -> ApiResponse:
    """Service for getting all categories."""

    # query
    query = db.session.query(Category).order_by(Category.id)

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    category_collection = [category.to_dict() for category in pagination]

    return ApiResponse(
        data={"categories": category_collection}, pagination=pagination
    ).json()


def category_service(category_id: int) -> ApiResponse:
    """Service for getting a category."""

    category = Category.query.get(category_id)

    if category is None:
        return ApiResponse(
            HttpRequestEnum.NOT_FOUND.value, message="category not found"
        ).json()

    return ApiResponse(data={"category": category.to_dict()}).json()


def tags_service(page: int = 1, per_page: int = 10) -> ApiResponse:
    """Service for getting all tags."""

    # query
    query = db.session.query(Tag).order_by(Tag.id)

    # pagination
    pagination = db.paginate(query, page=page, per_page=per_page)

    # convert to JSON data
    tags_collection = [tag.to_dict() for tag in pagination.items]

    return ApiResponse(data={"tags": tags_collection}, pagination=pagination).json()


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
