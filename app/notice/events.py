"""Notice events."""

import enum

from flask import current_app
from flask_login import current_user

from app.models.notice import NoticeActionEnum, NoticeModuleEnum

from . import notification_signal


class NoticeTypeEnum(enum.Enum):
    """Enum for notice type."""

    USER_RESET_PASSWORD = (
        f"{NoticeModuleEnum.USER.value}, {NoticeActionEnum.RESET_PASSWORD.value}"
    )

    USER_UPDATED_PROFILE = (
        f"{NoticeModuleEnum.USER.value}, {NoticeActionEnum.UPDATED_PROFILE.value}"
    )

    POST_CREATED = f"{NoticeModuleEnum.POST.value}, {NoticeActionEnum.CREATED.value}"
    POST_UPDATED = f"{NoticeModuleEnum.POST.value}, {NoticeActionEnum.UPDATED.value}"
    POST_DELETED = f"{NoticeModuleEnum.POST.value}, {NoticeActionEnum.DELETED.value}"

    COMMENT_CREATED = (
        f"{NoticeModuleEnum.COMMENT.value}, {NoticeActionEnum.CREATED.value}"
    )
    COMMENT_UPDATED = (
        f"{NoticeModuleEnum.COMMENT.value}, {NoticeActionEnum.UPDATED.value}"
    )
    COMMENT_DELETED = (
        f"{NoticeModuleEnum.COMMENT.value}, {NoticeActionEnum.DELETED.value}"
    )

    REPLY_CREATED = f"{NoticeModuleEnum.REPLY.value}, {NoticeActionEnum.CREATED.value}"
    REPLY_UPDATED = f"{NoticeModuleEnum.REPLY.value}, {NoticeActionEnum.UPDATED.value}"
    REPLY_DELETED = f"{NoticeModuleEnum.REPLY.value}, {NoticeActionEnum.DELETED.value}"

    LIKE_CREATED = f"{NoticeModuleEnum.LIKE.value}, {NoticeActionEnum.CREATED.value}"
    LIKE_CANCEL = f"{NoticeModuleEnum.LIKE.value}, {NoticeActionEnum.CANCELLED.value}"

    FOLLOW_CREATED = (
        f"{NoticeModuleEnum.FOLLOW.value}, {NoticeActionEnum.CREATED.value}"
    )

    FOLLOW_CANCEL = (
        f"{NoticeModuleEnum.FOLLOW.value}, {NoticeActionEnum.CANCELLED.value}"
    )

    SAVE_CREATED = f"{NoticeModuleEnum.SAVE.value}, {NoticeActionEnum.CREATED.value}"
    SAVE_CANCEL = f"{NoticeModuleEnum.SAVE.value}, {NoticeActionEnum.CANCELLED.value}"

    COMMUNITY_CREATED = (
        f"{NoticeModuleEnum.COMMUNITY.value}, {NoticeActionEnum.CREATED.value}"
    )

    COMMUNITY_UPDATED = (
        f"{NoticeModuleEnum.COMMUNITY.value}, {NoticeActionEnum.UPDATED.value}"
    )

    COMMUNITY_DELETED = (
        f"{NoticeModuleEnum.COMMUNITY.value}, {NoticeActionEnum.DELETED.value}"
    )

    SYSTEM = f"{NoticeModuleEnum.SYSTEM.value}, {NoticeActionEnum.ANNOUNCEMENT.value}"


def notice_event(
    user_id: str = "anonymity", notice_type: NoticeTypeEnum = NoticeTypeEnum.SYSTEM
) -> None:
    """Function to send notice event."""

    if current_user.is_authenticated:
        user_id = current_user.id

    current_app.logger.info(
        "Notice Event - user_id: %s, notice_type: %s", user_id, notice_type.value
    )
    notification_signal.send("app", user_id=user_id, notice_type=notice_type.value)
