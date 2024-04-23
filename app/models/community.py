"""Community model."""

from app.extensions import db
from app.utils import generate_time


class Community(db.Model):
    """Community model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    description = db.Column(db.String(500), default="")
    avatar = db.Column(db.String(300), default="")
    create_at = db.Column(db.DateTime, default=generate_time())
    update_at = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    def __init__(
        self, name: str, category: int, description: str = "", avatar: str = ""
    ) -> None:
        self.name = name
        self.category = category
        self.description = description
        self.avatar = avatar

    def __repr__(self) -> str:
        """Return a string representation of the community."""

        return f"<Community {self.name}>"

    # genrated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the community."""

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "avatar": self.avatar,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }
