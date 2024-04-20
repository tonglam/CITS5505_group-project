"""Notice model."""

import enum

from app.constants import NoticeTypeEnum
from app.extensions import db
from app.utils import generate_time


class NoticeReadStatusEnum(enum.Enum):
    """Enum for notice read status."""

    READ = True
    UNREAD = False


class NoticeSendStatusEnum(enum.Enum):
    """Enum for notice send status."""

    WAIT = "WAIT"
    SENT = "SENT"
    ERROR = "ERROR"


class Notice(db.Model):
    """Notice model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), default="")
    notice_type = db.Column(db.String(50), default=NoticeTypeEnum.SYSTEM.value)
    read_status = db.Column(db.Boolean, default=NoticeReadStatusEnum.UNREAD.value)
    send_status = db.Column(db.String(50), default=NoticeSendStatusEnum.WAIT.value)
    create_at = db.Column(db.DateTime, default=generate_time())
    update_at = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        user: str,
        subject: str,
        content: str = "",
        notice_type: str = NoticeTypeEnum.SYSTEM.value,
        read_status: bool = NoticeReadStatusEnum.UNREAD.value,
        send_status: str = NoticeSendStatusEnum.WAIT.value,
    ) -> None:
        """Initialize the notice."""

        self.user = user
        self.subject = subject
        self.content = content
        self.notice_type = notice_type
        self.read_status = read_status
        self.send_status = send_status

    def __repr__(self) -> str:
        """Return a string representation of the notice."""

        return f"<Notice {self.subject}>"

    # genrated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the notice."""

        return {
            "id": self.id,
            "user": self.user,
            "subject": self.subject,
            "content": self.content,
            "notice_type": self.notice_type,
            "read_status": self.read_status,
            "send_status": self.send_status,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }
