"""Community model."""

from app.extensions import db
from app.utils import generate_time


class Community(db.Model):
    """Community model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    description = db.Column(db.String(500))
    avatar = db.Column(db.String(300))
    create_at = db.Column(db.DateTime, default=generate_time())
    update_at = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    category = db.relationship("Category", backref=db.backref("communities", lazy=True))

    def __init__(
        self, name: str, category_id: int, description: str = "", avatar: str = ""
    ) -> None:
        self.name = name
        self.category_id = category_id
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
            "category_id": self.category_id,
            "description": self.description,
            "avatar": self.avatar,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }
