"""Notice model."""

import enum

from app.extensions import db
from app.utils import generate_time


class NoticeModuleEnum(enum.Enum):
    """Enum for notice module."""

    SYSTEM = "System"
    POST = "Post"
    COMMENT = "Comment"
    REPLY = "Reply"
    LIKE = "Like"
    FOLLOW = "Follow"
    SAVE = "Save"
    COMMUNITY = "Community"


class NoticeActionEnum(enum.Enum):
    """Enum for notice action."""

    CREATED = "Created"
    UPDATED = "Updated"
    DELETED = "Deleted"
    CANCELLED = "Cancelled"
    ANNOUNCEMENT = "Announcement"


class NoticeTypeEnum(enum.Enum):
    """Enum for notice type."""

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


class NoticeReadStatusEnum(enum.Enum):
    """Enum for notice read status."""

    READ = True
    UNREAD = False


class NoticeSendStatusEnum(enum.Enum):
    """Enum for notice send status."""

    WAIT = "Wait"
    SENT = "Sent"
    ERROR = "Error"


class Notice(db.Model):
    """Notice model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), default="")
    notice_type = db.Column(db.String(50), default=NoticeModuleEnum.SYSTEM.value)
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
        notice_type: str = NoticeModuleEnum.SYSTEM.value,
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
