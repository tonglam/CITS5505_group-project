"""Trending model"""

from app.extensions import db
from app.utils import generate_date, generate_time


class Trending(db.Model):
    """Trending model"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey("request.id"), nullable=False)
    title = db.Column(db.String(40), nullable=False)
    author = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    reply_num = db.Column(db.Integer, default=0)
    date = db.Column(db.String(10), default=generate_date())
    update_at = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    def __init__(
        self, request_id: int, title: str, author: str, reply_num: int = 0
    ) -> None:
        self.request_id = request_id
        self.title = title
        self.author = author
        self.reply_num = reply_num

    def __repr__(self) -> str:
        """Return a string representation of the trending."""
        return f"<Trending {self.title}>"

    # genrated by copilot
    def to_dict(self) -> dict:
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
