"""Notice model."""

import enum

from app.extensions import db
from app.utils import generate_time


class NoticeModuleEnum(enum.Enum):
    """Enum for notice module."""

    SYSTEM = "System"
    USER = "User"
    POST = "Post"
    COMMENT = "Comment"
    REPLY = "Reply"
    LIKE = "Like"
    FOLLOW = "Follow"
    SAVE = "Save"
    COMMUNITY = "Community"


class NoticeActionEnum(enum.Enum):
    """Enum for notice action."""

    RESET_PASSWORD = "Reset Password"
    UPDATED_PROFILE = "Updated Profile"
    CREATED = "Created"
    UPDATED = "Updated"
    DELETED = "Deleted"
    CANCELLED = "Cancelled"
    ANNOUNCEMENT = "Announcement"


class NoticeStatusEnum(enum.Enum):
    """Enum for notice read status."""

    READ = True
    UNREAD = False


class Notice(db.Model):
    """Notice model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), default="")
    notice_type = db.Column(db.String(50), default=NoticeModuleEnum.SYSTEM.value)
    status = db.Column(db.Boolean, default=NoticeStatusEnum.UNREAD.value)
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
        notice_type: str = NoticeModuleEnum.SYSTEM.value,
        status: bool = NoticeStatusEnum.UNREAD.value,
    ) -> None:
        """Initialize the notice."""

        self.user = user
        self.subject = subject
        self.content = content
        self.notice_type = notice_type
        self.status = status

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
            "status": self.status,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }
