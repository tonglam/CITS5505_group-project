"""Notice events."""

import enum

from blinker import Namespace
from flask import current_app, g
from flask_login import current_user

from app.constants import G_NOTICE_NUM
from app.extensions import db
from app.models.notice import (
    Notice,
    NoticeActionEnum,
    NoticeModuleEnum,
    NoticeStatusEnum,
)

_signals = Namespace()
_notification_signal = _signals.signal("notification")


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


def _handle_notification(_, **kwargs: dict) -> None:
    """Function to handle notification event."""

    user_id = kwargs.get("user_id")
    if not user_id:
        current_app.logger.error("User id is required for notification event")
        raise ValueError("User id is required")

    notice_type = kwargs.get("notice_type")
    notice_module = notice_type.split(", ")[0].strip()
    notice_action = notice_type.split(", ")[1].strip()
    current_app.logger.info(f"Received notification: {notice_module}, {notice_action}")

    if notice_module not in [module.value for module in NoticeModuleEnum]:
        current_app.logger.error(f"Invalid notice module: {notice_module}")
        raise ValueError(f"Invalid notice module: {notice_module}")

    if notice_action not in [action.value for action in NoticeActionEnum]:
        current_app.logger.error(f"Invalid notice action: {notice_action}")
        raise ValueError(f"Invalid notice action: {notice_action}")

    # insert to database
    notice = Notice(
        user=user_id,
        subject=f"Notification: {notice_module}",
        content=f"{notice_action} successfully!",
        notice_type=notice_module,
        status=NoticeStatusEnum.UNREAD.value,
    )

    db.session.add(notice)
    db.session.commit()
    current_app.logger.info(
        f"Notification: {notice_module}, {notice_action} inserted into database"
    )

    # update layout notification number
    notice_num = getattr(g, G_NOTICE_NUM, 0) + 1
    g.notice_num = min(notice_num, 99)
    current_app.logger.info(f"Notice number updated: [{g.notice_num}]")


_notification_signal.connect(_handle_notification)


def notice_event(
    user_id: str = "anonymity", notice_type: NoticeTypeEnum = NoticeTypeEnum.SYSTEM
) -> None:
    """Function to send notice event."""

    if current_user.is_authenticated:
        user_id = current_user.id

    _notification_signal.send("app", user_id=user_id, notice_type=notice_type.value)
