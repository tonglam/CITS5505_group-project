"""Notice events."""

import enum

from flask import current_app, g
from flask_login import current_user

from app.models.user_notice import UserNoticeActionEnum, UserNoticeModuleEnum

from . import notification_signal


class NoticeTypeEnum(enum.Enum):
    """Enum for notice type."""

    USER_RESET_PASSWORD = f"{UserNoticeModuleEnum.USER.value}, \
        {UserNoticeActionEnum.RESET_PASSWORD.value}"

    USER_UPDATED_PROFILE = f"{UserNoticeModuleEnum.USER.value}, \
        {UserNoticeActionEnum.UPDATED_PROFILE.value}"

    USER_UPDATED_AVATAR = f"{UserNoticeModuleEnum.USER.value}, \
        {UserNoticeActionEnum.UPDATED_AVATAR.value}"

    COMMUNITY_JOIN = f"{UserNoticeModuleEnum.COMMUNITY.value}, \
        {UserNoticeActionEnum.JOINED.value}"

    COMMUNITY_LEAVE = f"{UserNoticeModuleEnum.COMMUNITY.value}, \
        {UserNoticeActionEnum.LEAVE.value}"

    COMMUNITY_CREATED = (
        f"{UserNoticeModuleEnum.COMMUNITY.value}, {UserNoticeActionEnum.CREATED.value}"
    )

    COMMUNITY_UPDATED = (
        f"{UserNoticeModuleEnum.COMMUNITY.value}, {UserNoticeActionEnum.UPDATED.value}"
    )

    COMMUNITY_DELETED = (
        f"{UserNoticeModuleEnum.COMMUNITY.value}, {UserNoticeActionEnum.DELETED.value}"
    )

    POST_CREATED = (
        f"{UserNoticeModuleEnum.POST.value}, {UserNoticeActionEnum.CREATED.value}"
    )
    POST_UPDATED = (
        f"{UserNoticeModuleEnum.POST.value}, {UserNoticeActionEnum.UPDATED.value}"
    )
    POST_DELETED = (
        f"{UserNoticeModuleEnum.POST.value}, {UserNoticeActionEnum.DELETED.value}"
    )

    REPLY_CREATED = (
        f"{UserNoticeModuleEnum.REPLY.value}, {UserNoticeActionEnum.CREATED.value}"
    )
    REPLY_UPDATED = (
        f"{UserNoticeModuleEnum.REPLY.value}, {UserNoticeActionEnum.UPDATED.value}"
    )
    REPLY_DELETED = (
        f"{UserNoticeModuleEnum.REPLY.value}, {UserNoticeActionEnum.DELETED.value}"
    )

    LIKE_CREATED = (
        f"{UserNoticeModuleEnum.LIKE.value}, {UserNoticeActionEnum.CREATED.value}"
    )
    LIKE_CANCEL = (
        f"{UserNoticeModuleEnum.LIKE.value}, {UserNoticeActionEnum.CANCELLED.value}"
    )

    SAVE_CREATED = (
        f"{UserNoticeModuleEnum.SAVE.value}, {UserNoticeActionEnum.CREATED.value}"
    )
    SAVE_CANCEL = (
        f"{UserNoticeModuleEnum.SAVE.value}, {UserNoticeActionEnum.CANCELLED.value}"
    )

    SYSTEM = f"{UserNoticeModuleEnum.SYSTEM.value}, {UserNoticeActionEnum.ANNOUNCEMENT.value}"


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
    g.notice_num += 1
