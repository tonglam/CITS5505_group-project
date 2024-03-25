"""Trending model"""

from sqlalchemy import event

from app.extensions import db
from app.utils import generate_date, generate_time


# pylint: disable=too-few-public-methods
class Trending(db.Model):
    """Trending model"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey("request.id"), nullable=False)
    title = db.Column(db.String(40), nullable=False)
    author = db.Column(db.String(36), db.ForeignKey("user.userId"), nullable=False)
    reply_num = db.Column(db.Integer, default=0)
    date = db.Column(db.String(10), default=generate_date())
    update_at = db.Column(db.DateTime, default=generate_time())

    def __init__(
        self, request_id: int, title: str, author: str, reply_num: int = 0
    ) -> None:
        self.request_id = request_id
        self.title = title
        self.author = author
        self.reply_num = reply_num

    def __repr__(self) -> str:
        return f"<Trending {self.title}>"

    # genrated by copilot
    def to_dict(self):
        """Return a JSON format of the trending."""
        return {
            "id": self.id,
            "request_id": self.request_id,
            "title": self.title,
            "author": self.author,
            "reply_num": self.reply_num,
            "date": self.date,
            "update_at": self.update_at,
        }


# pylint: disable=unused-argument
@event.listens_for(Trending, "before_insert")
def before_insert_listener(mapper, connect, target):
    """Update the create time before inserting a new trending."""

    target.update_at = generate_time()


@event.listens_for(Trending, "before_update")
def before_update_listener(mapper, connect, target):
    """Update the update time before updating a trending."""

    target.update_at = generate_time()
