"""This module contains the service layer for the community app."""

from werkzeug.datastructures import FileStorage

from app.api.service import upload_image_service
from app.constants import HttpRequestEnum
from app.models.community import Community

from .forms import CommunityForm


def create_community_service(form: CommunityForm) -> dict:
    """Create a new community."""

    if form is None:
        return {
            "code": HttpRequestEnum.BAD_REQUEST.value,
            "message": "Create community failed, invalid form.",
        }

    # get form data
    avatar_file = form.avatar.data
    name = form.name.data
    description = form.description.data
    category_id = form.category_select.data
    creator_id = form.creator_id.data

    # get avatar url
    upload_avatar_url = get_upload_avatar_url(avatar_file)

    community = Community(
        name=name,
        category_id=category_id,
        description=description,
        avatar_url=upload_avatar_url,
        creator_id=creator_id,
    )

    return {
        "code": HttpRequestEnum.CREATED.value,
        "data": community,
    }


def update_community_service(community: Community, form: CommunityForm) -> dict:
    """Update a community."""

    if community is None:
        return {
            "code": HttpRequestEnum.NOT_FOUND.value,
            "message": "Community not found.",
        }

    if form is None:
        return {"code": HttpRequestEnum.BAD_REQUEST.value, "message": "Invalid form."}

    # get form data
    avatar_file = form.avatar.data
    name = form.name.data
    description = form.description.data
    category_id = form.category_select.data

    # update community
    update = False

    # get avatar url
    if avatar_file:
        upload_avatar_url = get_upload_avatar_url(avatar_file)
        community.avatar_url = upload_avatar_url
        update = True

    if community.name != name:
        community.name = name
        update = True

    if community.category_id != category_id:
        community.category_id = category_id
        update = True

    if community.description != description:
        community.description = description
        update = True

    if update:
        return {
            "code": HttpRequestEnum.SUCCESS_OK.value,
            "data": community,
        }

    return {"code": HttpRequestEnum.SUCCESS_OK.value, "data": None}


def get_upload_avatar_url(avatar_file: FileStorage):
    """Get upload avatar url."""

    upload_avatar_response = upload_image_service(avatar_file).get_json()
    if upload_avatar_response.get("code") != HttpRequestEnum.SUCCESS_OK.value:
        return None
    return upload_avatar_response.get("data").get("image_url")
