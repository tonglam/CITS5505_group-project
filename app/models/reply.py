"""Reply model."""

import enum

from app.extensions import db
from app.utils import generate_time


class ReplySourceEnum(enum.Enum):
    """Enum for reply source."""

    HUMAN = "HUMAN"
    AI = "AI"


class Reply(db.Model):
    """Reply model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request = db.Column(db.Integer, db.ForeignKey("request.id"), nullable=False)
    replier = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String(1000))
    source = db.Column(
        db.String(50), db.Enum(ReplySourceEnum), default=ReplySourceEnum.HUMAN.value
    )
    like_num = db.Column(db.Integer)
    save_num = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=generate_time())
    update_at = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        request: int,
        replier: str,
        content: str,
        source: str,
        like_num: int,
        save_num: int,
    ) -> None:
        self.request = request
        self.replier = replier
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
            "request": self.request,
            "replier": self.replier,
            "content": self.content,
            "source": self.source,
            "like_num": self.like_num,
            "save_num": self.save_num,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }
