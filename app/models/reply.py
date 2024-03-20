"""Reply model."""

from sqlalchemy import event

from app.extensions import db
from app.utils import generate_time


# pylint: disable=too-few-public-methods
class Reply(db.Model):
    """Reply model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request = db.Column(db.Integer, db.ForeignKey("request.id"), nullable=False)
    replier = db.Column(db.String(36), db.ForeignKey("user.userId"), nullable=False)
    content = db.Column(db.String(1000), default="")
    source = db.Column(db.String(50), default="human")
    like_num = db.Column(db.Integer, default=0)
    save_num = db.Column(db.Integer, default=0)
    create_at = db.Column(db.DateTime, default=generate_time())
    update_at = db.Column(db.DateTime, default=generate_time())

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        request: int,
        replier: str,
        content: str = "",
        source: str = "human",
        like_num: int = 0,
        save_num: int = 0,
    ) -> None:
        self.request = request
        self.replier = replier
        self.content = content
        self.source = source
        self.like_num = like_num
        self.save_num = save_num

    def __repr__(self) -> str:
        return f"<Reply {self.content}>"


# pylint: disable=unused-argument
@event.listens_for(Reply, "before_insert")
def before_insert_listener(mapper, connect, target):
    """Update the create time before inserting a new reply."""

    target.create_at = generate_time()
    target.update_at = generate_time()


@event.listens_for(Reply, "before_update")
def before_update_listener(mapper, connect, target):
    """Update the update time before updating a reply."""

    target.update_at = generate_time()
