"""Service for searching."""

from sqlalchemy.orm import joinedload

from app.models.community import Community
from app.models.reply import Reply
from app.models.request import Request
from app.models.user import User


def search_service(keyword: str = None) -> dict:
    """Service for searching requests by keyword."""

    if not keyword:
        return None

    keyword = "%" + keyword + "%"

    search_results = {}

    # community
    community_results = community_search_result(keyword)
    search_results["community"] = community_results

    # request
    request_results = request_search_result(keyword)
    search_results["request"] = request_results

    # reply
    reply_results = reply_search_result(keyword)
    search_results["reply"] = reply_results

    return search_results


def community_search_result(keyword: str = None) -> list:
    """Service for searching community by keyword."""

    # name
    community_names = Community.query.filter(Community.name.like(keyword)).all()
    community_name_result = [
        {
            "id": community.id,
            "highlight": "name",
            "name": community.name,
            "description": community.description,
            "creator": "tonglam",
        }
        for community in community_names
    ]

    # description
    community_descriptions = Community.query.filter(
        Community.description.like(keyword)
    ).all()
    community_description_result = [
        {
            "id": community.id,
            "highlight": "description",
            "name": community.name,
            "description": community.description,
            "creator": "tonglam",
        }
        for community in community_descriptions
    ]

    return community_name_result + community_description_result


def request_search_result(keyword: str = None) -> list:
    """Service for searching requests by keyword."""

    # title
    request_titles = Request.query.filter(Request.title.like(keyword)).all()
    request_title_result = [
        {
            "id": request.id,
            "highlight": "title",
            "title": request.title,
            "content": request.content,
            "author": request.author.username,
        }
        for request in request_titles
    ]

    # content
    request_contents = Request.query.filter(Request.content.like(keyword)).all()
    request_content_result = [
        {
            "id": request.id,
            "highlight": "content",
            "title": request.title,
            "content": request.content,
            "author": request.author.username,
        }
        for request in request_contents
    ]

    # author
    request_authors = (
        Request.query.join(User, Request.author_id == User.id)
        .filter(User.username.like(keyword))
        .options(joinedload(Request.author))
        .all()
    )
    request_author_result = [
        {
            "id": request.id,
            "highlight": "author",
            "title": request.title,
            "content": request.content,
            "author": request.author.username,
        }
        for request in request_authors
    ]

    return request_title_result + request_content_result + request_author_result


def reply_search_result(keyword: str = None) -> list:
    """Service for searching replies by keyword."""

    # content
    reply_contents = Reply.query.filter(Reply.content.like(keyword)).all()
    reply_content_result = [
        {
            "id": reply.id,
            "highlight": "content",
            "title": reply.request.title,
            "content": reply.content,
            "replier": reply.replier.username,
        }
        for reply in reply_contents
    ]

    # replier
    reply_repliers = (
        Reply.query.join(User, Reply.replier_id == User.id)
        .filter(User.username.like(keyword))
        .options(joinedload(Reply.replier))
        .all()
    )
    reply_replier_result = [
        {
            "id": reply.id,
            "highlight": "replier",
            "title": reply.request.title,
            "content": reply.content,
            "replier": reply.replier.username,
        }
        for reply in reply_repliers
    ]

    return reply_content_result + reply_replier_result
