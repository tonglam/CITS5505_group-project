"""Model for Type."""

from sqlalchemy import event

from app.extensions import db
from app.utils import generate_time


# pylint: disable=too-few-public-methods
class Tag(db.Model):
    """Type model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_at = db.Column(db.DateTime, default=generate_time())

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Type {self.name}>"


# pylint: disable=unused-argument
@event.listens_for(Tag, "before_insert")
def before_insert_listener(mapper, connect, target):
    """Update the create time before inserting a new type."""

    target.create_at = generate_time()
