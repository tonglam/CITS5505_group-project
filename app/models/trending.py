"""Trending model"""

import datetime

from app.extensions import db
from app.utils import (format_datetime_to_readable_string, generate_date,
                       generate_time)


class Trending(db.Model):
    """Trending model"""

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id: int = db.Column(
        db.Integer, db.ForeignKey("request.id"), unique=True, nullable=False
    )
    author_id: str = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    view_num: int = db.Column(db.Integer, default=0)
    reply_num: int = db.Column(db.Integer, default=0)
    date: str = db.Column(db.String(10), default=generate_date())
    update_at: datetime = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    request = db.relationship("Request", backref=db.backref("trendings", lazy=True))
    author = db.relationship("User", backref=db.backref("trendings", lazy=True))

    def __init__(
        self, request_id: int, author_id: str, view_num: int = 0, reply_num: int = 0
    ) -> None:
        self.request_id = request_id
        self.author_id = author_id
        self.view_num = view_num
        self.reply_num = reply_num

    def __repr__(self) -> str:
        """Return a string representation of the trending."""

        return f"<Trending {self.request_id}>"

    # generated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the trending."""

        return {
            "id": self.id,
            "request": self.request.to_dict() if self.request else None,
            "author": self.author.to_dict() if self.author else None,
            "view_num": self.view_num,
            "reply_num": self.reply_num,
            "date": self.date,
            "update_at": format_datetime_to_readable_string(self.update_at),
        }
