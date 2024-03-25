"""UserPreference model."""

import datetime

from sqlalchemy import event

from app.extensions import db
from app.utils import generate_time


# pylint: disable=too-few-public-methods
class UserPreference(db.Model):
    """UserPreference model."""

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: str = db.Column(
        db.String(36), db.ForeignKey("user.userId"), nullable=False
    )
    communities: str = db.Column(db.String(80), default="")
    interests: str = db.Column(db.String(80), default="")
    update_at: datetime = db.Column(db.DateTime, default=generate_time())

    def __init__(
        self, user_id: str, communities: str = "", interests: str = ""
    ) -> None:
        self.user_id = user_id
        self.communities = communities
        self.interests = interests

    def __repr__(self) -> str:
        return f"<UserPreference {self.user_id}>"

    # genrated by copilot
    def to_dict(self):
        """Return a JSON format of the user preference."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "communities": self.communities,
            "interests": self.interests,
            "update_at": self.update_at,
        }


# pylint: disable=unused-argument
@event.listens_for(UserPreference, "before_insert")
def before_insert_listener(mapper, connect, target):
    """Update the create time before inserting a new user preference."""

    target.update_at = generate_time()


@event.listens_for(UserPreference, "before_update")
def before_update_listener(mapper, connect, target):
    """Update the update time before updating a user preference."""

    target.update_at = generate_time()
