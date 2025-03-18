"""This module contains the service functions for the popular blueprint."""

from sqlalchemy import func

from app.constants import TOP_COMMUNITY_NUM, TOP_DATA_NUM
from app.extensions import db
from app.models import Category, Community, Reply, Request, UserRecord


def top_replied_service():
    """Return the top replied requests."""

    # pylint: disable=not-callable
    top_replied = (
        db.session.query(
            Reply.request_id, func.count(Reply.request_id).label("reply_count")
        )
        .group_by(Reply.request_id)
        .order_by(func.count(Reply.request_id).desc())
        .limit(TOP_DATA_NUM)
        .all()
    )

    # Get the request details for each top replied request
    top_replied_info = []
    for reply in top_replied:
        request = Request.query.get(reply.request_id)
        if request:
            top_replied_info.append(
                {
                    "id": request.id,
                    "username": request.author.username,
                    "title": request.title,
                }
            )

    return top_replied_info


def top_viewed_service():
    """Return the top viewed requests."""

    # pylint: disable=not-callable
    top_viewed = (
        db.session.query(
            UserRecord.request_id, func.count(UserRecord.request_id).label("view_count")
        )
        .group_by(UserRecord.request_id)
        .order_by(func.count(UserRecord.request_id).desc())
        .limit(TOP_DATA_NUM)
        .all()
    )

    # Get the request details for each top viewed request
    top_viewed_info = []
    for record in top_viewed:
        request = Request.query.get(record.request_id)
        if request:
            top_viewed_info.append(
                {
                    "id": request.id,
                    "username": request.author.username,
                    "title": request.title,
                }
            )

    return top_viewed_info


def top_community_service():
    """Return the top communities"""

    # pylint: disable=not-callable
    top_community = (
        db.session.query(
            Request.community_id, func.count(Request.id).label("request_count")
        )
        .group_by(Request.community_id)
        .order_by(func.count(Request.id).desc())
        .limit(TOP_COMMUNITY_NUM)
        .all()
    )

    community_category = db.session.query(Category).all()
    community_category_dict = {
        category.id: category.name for category in community_category
    }

    # Get the community details for each top community
    top_community_info = []
    for request in top_community:
        community = Community.query.get(request.community_id)
        if community:
            top_community_info.append(
                {
                    "id": community.id,
                    "community": community.name,
                    "category": community_category_dict.get(
                        community.category_id, "Unknown"
                    ),
                }
            )

    return top_community_info
