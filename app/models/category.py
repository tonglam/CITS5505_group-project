"""Category model."""

from sqlalchemy import event

from app.extensions import db
from app.utils import generate_time


# pylint: disable=too-few-public-methods
class Category(db.Model):
    """Category model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_at = db.Column(db.DateTime, default=generate_time())

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Category {self.name}>"

    # genrated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the category."""
        return {
            "id": self.id,
            "name": self.name,
            "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


# pylint: disable=unused-argument
@event.listens_for(Category, "before_insert")
def before_insert_listener(mapper, connect, target):
    """Update the create time before inserting a new category."""
    target.create_at = generate_time()
