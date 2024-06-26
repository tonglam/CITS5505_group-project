"""User Preference model."""

import datetime

from app.extensions import db
from app.utils import format_datetime_to_readable_string, generate_time


class UserPreference(db.Model):
    """User Preference model."""

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: str = db.Column(
        db.String(36), db.ForeignKey("user.id"), unique=True, nullable=False
    )
    communities: str = db.Column(db.String(200))
    interests: str = db.Column(db.String(200))
    update_at: datetime = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    user = db.relationship("User", backref=db.backref("user_preference", lazy=True))

    def __init__(
        self, user_id: str, communities: str = "", interests: str = ""
    ) -> None:
        self.user_id = user_id
        self.communities = communities
        self.interests = interests

    def __repr__(self) -> str:
        """Return a string representation of the user preference."""

        return f"<UserPreference {self.user_id}>"

    # generated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the user preference."""

        return {
            "id": self.id,
            "user": self.user.to_dict() if self.user else None,
            "communities": self.communities,
            "interests": self.interests,
            "update_at": format_datetime_to_readable_string(self.update_at),
        }
