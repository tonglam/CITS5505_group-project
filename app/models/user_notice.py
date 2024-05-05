"""User Notice model."""

import datetime
import enum

from app.extensions import db
from app.utils import generate_time


class UserNoticeModuleEnum(enum.Enum):
    """Enum for User Notice module."""

    SYSTEM = "SYSTEM"
    USER = "USER"
    POST = "POST"
    COMMENT = "COMMENT"
    REPLY = "REPLY"
    LIKE = "LIKE"
    FOLLOW = "FOLLOW"
    SAVE = "SAVE"
    COMMUNITY = "COMMUNITY"


class UserNoticeActionEnum(enum.Enum):
    """Enum for user notice action."""

    RESET_PASSWORD = "RESET_PASSWORD"
    UPDATED_PROFILE = "UPDATED_PROFILE"
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    DELETED = "DELETED"
    CANCELLED = "CANCELLED"
    ANNOUNCEMENT = "ANNOUNCEMENT"


class UserNotice(db.Model):
    """User Notice model."""

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: str = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    subject: str = db.Column(db.String(100), nullable=False)
    content: str = db.Column(db.String(1000), default="")
    module: UserNoticeModuleEnum = db.Column(
        db.Enum(UserNoticeModuleEnum), default=UserNoticeModuleEnum.SYSTEM
    )
    status: bool = db.Column(db.Boolean, default=False)
    create_at: datetime = db.Column(db.DateTime, default=generate_time())
    update_at: datetime = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    user = db.relationship("User", backref=db.backref("notices", lazy=True))

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        user_id: str,
        subject: str,
        content: str = "",
        module: str = UserNoticeModuleEnum.SYSTEM,
        status: bool = False,
    ) -> None:
        """Initialize the user notice."""

        self.user_id = user_id
        self.subject = subject
        self.content = content
        self.module = module
        self.status = status

    def __repr__(self) -> str:
        """Return a string representation of the user notice."""

        return f"<Notice {self.id}>"

    # genrated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the user notice."""

        return {
            "id": self.id,
            "user_id": self.user_id,
            "subject": self.subject,
            "content": self.content,
            "module": self.module.value,
            "status": self.status,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }