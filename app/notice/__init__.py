# pylint: skip-file


from blinker import Namespace
from flask import Blueprint, current_app, g

from app.constants import G_NOTICE_NUM
from app.extensions import db
from app.models.notice import (
    Notice,
    NoticeActionEnum,
    NoticeModuleEnum,
    NoticeStatusEnum,
)

signals = Namespace()
notification_signal = signals.signal("notification")

notice_bp = Blueprint(
    "notice",
    __name__,
    template_folder="templates",
    static_folder="static",
)


def handle_notification(_, **kwargs: dict) -> None:
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


notification_signal.connect(handle_notification)

from . import routes
