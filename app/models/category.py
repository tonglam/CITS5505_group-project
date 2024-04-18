"""Category model."""

from app.extensions import db
from app.utils import generate_time


class Category(db.Model):
    """Category model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_at = db.Column(db.DateTime, default=generate_time())

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        """Return a string representation of the category."""
        return f"<Category {self.name}>"

    # genrated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the category."""
        return {
            "id": self.id,
            "name": self.name,
            "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
