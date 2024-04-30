"""Trending model"""

from app.extensions import db
from app.utils import generate_date, generate_time


class Trending(db.Model):
    """Trending model"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(
        db.Integer, db.ForeignKey("request.id"), unique=True, nullable=False
    )
    request_title = db.Column(db.String(40), db.ForeignKey("request.title"))
    author_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    reply_num = db.Column(db.Integer, default=0)
    date = db.Column(db.String(10), default=generate_date())
    update_at = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    request = db.relationship("Request", backref=db.backref("trendings", lazy=True))
    author = db.relationship("User", backref=db.backref("trendings", lazy=True))

    def __init__(
        self, request_id: int, title: str, author_id: str, reply_num: int = 0
    ) -> None:
        self.request_id = request_id
        self.request_title = title
        self.author_id = author_id
        self.reply_num = reply_num

    def __repr__(self) -> str:
        """Return a string representation of the trending."""

        return f"<Trending {self.request_id}>"

    # genrated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the trending."""

        return {
            "id": self.id,
            "request_id": self.request_id,
            "title": self.request_title,
            "author_id": self.author_id,
            "reply_num": self.reply_num,
            "date": self.date,
            "update_at": self.update_at,
        }
