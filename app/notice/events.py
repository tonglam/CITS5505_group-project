"""Notice events."""

from blinker import Namespace
from flask import current_app
from flask_login import current_user

from app.extensions import db
from app.models.notice import (
    Notice,
    NoticeActionEnum,
    NoticeModuleEnum,
    NoticeReadStatusEnum,
    NoticeSendStatusEnum,
    NoticeTypeEnum,
)

signals = Namespace()
notification_signal = signals.signal("notification")


def handle_notification(_, **kwargs: dict) -> None:
    """Function to handle notification event."""

    user_id = kwargs.get("user_id")
    if not user_id:
        current_app.logger.error("User id is required for notification event")
        raise ValueError("User id is required")

    notice_type = kwargs.get("notice_type")
    print("notice_type: ", notice_type)

    notice_module = notice_type.split(", ")[0].strip()
    print("notice_module: ", notice_module)
    notice_action = notice_type.split(", ")[1].strip()
    print("notice_action: ", notice_action)

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
        read_status=NoticeReadStatusEnum.UNREAD.value,
        send_status=NoticeSendStatusEnum.WAIT.value,
    )

    print("Notice: ", notice.to_dict())

    db.session.add(notice)
    db.session.commit()

    # update layout notification


notification_signal.connect(handle_notification)


def notice_event(
    user_id: str = "anonymity", notice_type: NoticeTypeEnum = NoticeTypeEnum.SYSTEM
) -> None:
    """Function to send notice event."""

    if current_user.is_authenticated:
        user_id = current_user.id

    print("user_id: ", user_id)

    notification_signal.send("app", user_id=user_id, notice_type=notice_type.value)
