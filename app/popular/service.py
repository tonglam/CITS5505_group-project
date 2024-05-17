"""This module contains the service functions for the popular blueprint."""

from sqlalchemy import func

from app.constants import TOP_COMMUNITY_NUM, TOP_DATA_NUM
from app.extensions import db
from app.models import Category, Reply, Request, UserRecord


def top_replied_service():
    """Return the top replied requests."""

    # pylint: disable=not-callable
    top_replied = (
        db.session.query(Reply)
        .group_by(Reply.request_id)
        .order_by(func.count(Reply.request_id))
        .limit(TOP_DATA_NUM)
        .all()
    )

    top_replied_info = [
        {
            "id": reply.request.id,
            "username": reply.request.author.username,
            "title": reply.request.title,
        }
        for reply in top_replied
    ]

    return top_replied_info


def top_viewed_service():
    """Return the top viewed requests."""

    # pylint: disable=not-callable
    top_viewed = (
        db.session.query(UserRecord)
        .group_by(UserRecord.request_id)
        .order_by(func.count(UserRecord.request_id))
        .limit(TOP_DATA_NUM)
        .all()
    )

    top_viewed_info = [
        {
            "id": record.request.id,
            "username": record.request.author.username,
            "title": record.request.title,
        }
        for record in top_viewed
    ]

    return top_viewed_info


def top_community_service():
    """Return the top communities"""

    # pylint: disable=not-callable
    top_community = (
        db.session.query(Request)
        .group_by(Request.community_id)
        .order_by(func.count(Request.id))
        .limit(TOP_COMMUNITY_NUM)
        .all()
    )

    community_category = db.session.query(Category).all()
    community_category_dict = {
        category.id: category.name for category in community_category
    }

    top_community_info = [
        {
            "id": request.id,
            "community": request.community.name,
            "category": community_category_dict[request.community.category_id],
            "description": request.community.description,
        }
        for request in top_community
    ]

    return top_community_info
