"""UserPreference model."""

from app.extensions import db
from app.utils import generate_time


# pylint: disable=too-few-public-methods
class UserPreference(db.Model):
    """UserPreference model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    communities = db.Column(db.String(80), default="")
    interests = db.Column(db.String(80), default="")
    update_at = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

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
