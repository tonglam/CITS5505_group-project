"""Model for Tag."""

from app.extensions import db
from app.utils import generate_time


class Tag(db.Model):
    """Tag model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    create_at = db.Column(db.DateTime, default=generate_time())

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"

    # genrated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the tag."""

        return {
            "id": self.id,
            "name": self.name,
            "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
