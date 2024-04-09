"""UserRecord model."""

from app import constant
from app.extensions import db
from app.utils import generate_time


# pylint: disable=too-few-public-methods
class UserRecord(db.Model):
    """UserRecord model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey("request.id"), nullable=False)
    record_type = db.Column(
        db.String(80),
        db.Enum(constant.UserRecordEnum),
        default=constant.UserRecordEnum.VIEW,
    )
    update_at = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    def __init__(
        self, user_id: str, request_id: str, record_type: constant.UserRecordEnum
    ) -> None:
        self.user_id = user_id
        self.request_id = request_id
        self.record_type = record_type

    def __repr__(self) -> str:
        return f"<UserRecord {self.user_id}>"

    # genrated by copilot
    def to_dict(self):
        """Return a JSON format of the user record."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "request_id": self.request_id,
            "record_type": self.record_type,
            "update_at": self.update_at,
        }
