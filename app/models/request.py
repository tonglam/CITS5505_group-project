"""Request model."""

from sqlalchemy import event

from app.extensions import db
from app.utils import generate_time


# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
class Request(db.Model):
    """Request model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    community = db.Column(db.Integer, db.ForeignKey("community.id"), nullable=False)
    author = db.Column(db.String(36), db.ForeignKey("user.user_id"), nullable=False)
    title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.String(1000), default="")
    tag = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=True)
    view_num = db.Column(db.Integer, default=0)
    like_num = db.Column(db.Integer, default=0)
    reply_num = db.Column(db.Integer, default=0)
    save_num = db.Column(db.Integer, default=0)
    create_at = db.Column(db.DateTime, default=generate_time())
    update_at = db.Column(db.DateTime, default=generate_time())

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        community: int,
        author: str,
        title: str,
        content: str = "",
        tag: int = None,
        view_num: int = 0,
        like_num: int = 0,
        reply_num: int = 0,
        save_num: int = 0,
    ) -> None:
        self.community = community
        self.author = author
        self.title = title
        self.content = content
        self.tag = tag
        self.view_num = view_num
        self.like_num = like_num
        self.reply_num = reply_num
        self.save_num = save_num

    def __repr__(self) -> str:
        return f"<Request {self.title}>"

    # genrated by copilot
    def to_dict(self):
        """Return a JSON format of the request."""
        return {
            "id": self.id,
            "community": self.community,
            "author": self.author,
            "title": self.title,
            "content": self.content,
            "tag": self.tag,
            "view_num": self.view_num,
            "like_num": self.like_num,
            "reply_num": self.reply_num,
            "save_num": self.save_num,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }


# pylint: disable=unused-argument
@event.listens_for(Request, "before_insert")
def before_insert_listener(mapper, connect, target):
    """Update the create time before inserting a new request."""
    target.create_at = generate_time()
    target.update_at = generate_time()


@event.listens_for(Request, "before_update")
def before_update_listener(mapper, connect, target):
    """Update the update time before updating a request."""
    target.update_at = generate_time()
