"""Reply model."""

import datetime
import enum

from app.extensions import db
from app.utils import generate_time


class ReplySourceEnum(enum.Enum):
    """Enum for reply source."""

    HUMAN = "HUMAN"
    AI = "AI"


class Reply(db.Model):
    """Reply model."""

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id: int = db.Column(db.Integer, db.ForeignKey("request.id"), nullable=False)
    replier_id: str = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    content: str = db.Column(db.String(1000))
    source: ReplySourceEnum = db.Column(
        db.Enum(ReplySourceEnum), default=ReplySourceEnum.HUMAN.value
    )
    like_num: int = db.Column(db.Integer, default=0)
    save_num: int = db.Column(db.Integer, default=0)
    create_at: datetime = db.Column(db.DateTime, default=generate_time())
    update_at: datetime = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    request = db.relationship("Request", backref=db.backref("replies", lazy=True))
    replier = db.relationship("User", backref=db.backref("replies", lazy=True))

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        request_id: int,
        replier_id: str,
        content: str,
        source: str,
        like_num: int,
        save_num: int,
    ) -> None:
        self.request_id = request_id
        self.replier_id = replier_id
        self.content = content
        self.source = source
        self.like_num = like_num
        self.save_num = save_num

    def __repr__(self) -> str:
        """Return a string representation of the reply."""

        return f"<Reply {self.id}>"

    # genrated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the reply."""

        return {
            "id": self.id,
            "request_id": self.request_id,
            "replier_id": self.replier_id,
            "content": self.content,
            "source": self.source.value,
            "like_num": self.like_num,
            "save_num": self.save_num,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }
