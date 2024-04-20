"""Notice events."""

from blinker import Namespace
from flask import current_app

from app.models.notice import NoticeTypeEnum

signals = Namespace()
notification_signal = signals.signal("notification")


def handle_notification(_, **kwargs: dict) -> None:
    """Function to handle notification event."""

    notice_type = kwargs.get("type")
    if notice_type not in [type.value for type in NoticeTypeEnum]:
        current_app.logger.error(f"Invalid notice type: {notice_type}")
        raise ValueError(f"Invalid notice type: {notice_type}")

    event_data = kwargs.get("data")
    current_app.logger.info(f"Notification: {notice_type} - {event_data}")


notification_signal.connect(handle_notification)


def notice_event(
    notice_type: NoticeTypeEnum = NoticeTypeEnum.SYSTEM, notice_data: dict = None
) -> None:
    """Function to send notice event."""

    notification_signal.send("app", type=notice_type.value, data=notice_data)
