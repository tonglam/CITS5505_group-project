"""UserRecord model."""

import datetime
import enum

from app.extensions import db
from app.utils import generate_time


class UserRecordTypeEnum(enum.Enum):
    """Enum for user record."""

    REQUEST = "REQUEST"
    REPLY = "REPLY"
    VIEW = "VIEW"
    LIKE = "LIKE"
    SAVE = "SAVE"


class UserRecord(db.Model):
    """UserRecord model."""

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: str = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    request_id: int = db.Column(db.Integer, db.ForeignKey("request.id"), nullable=False)
    record_type: UserRecordTypeEnum = db.Column(
        db.Enum(UserRecordTypeEnum),
        default=UserRecordTypeEnum.VIEW,
    )
    update_at: datetime = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    user = db.relationship("User", backref=db.backref("user_records", lazy=True))
    request = db.relationship("Request", backref=db.backref("user_records", lazy=True))

    def __init__(
        self, user_id: str, request_id: str, record_type: UserRecordTypeEnum
    ) -> None:
        self.user_id = user_id
        self.request_id = request_id
        self.record_type = record_type

    def __repr__(self) -> str:
        """Return a string representation of the user record."""

        return f"<UserRecord {self.id}>"

    # genrated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the user record."""

        return {
            "id": self.id,
            "user_id": self.user_id,
            "request_id": self.request_id,
            "record_type": self.record_type.value,
            "update_at": self.update_at,
        }
