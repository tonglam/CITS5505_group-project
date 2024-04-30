"""Request model."""

from app.extensions import db
from app.utils import generate_time


# pylint: disable=too-many-instance-attributes
class Request(db.Model):
    """Request model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.String(1000), default="")
    community_id = db.Column(db.Integer, db.ForeignKey("community.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    view_num = db.Column(db.Integer)
    like_num = db.Column(db.Integer)
    reply_num = db.Column(db.Integer)
    save_num = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=generate_time())
    update_at = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    author = db.relationship("User", backref=db.backref("requests", lazy=True))
    community = db.relationship("Community", backref=db.backref("requests", lazy=True))
    category = db.relationship("Category", backref=db.backref("requests", lazy=True))

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        author_id: str,
        title: str,
        content: str,
        community: int,
        category: int,
        view_num: int,
        like_num: int,
        reply_num: int,
        save_num: int,
    ) -> None:
        self.author_id = author_id
        self.title = title
        self.content = content
        self.community = community
        self.category = category
        self.view_num = view_num
        self.like_num = like_num
        self.reply_num = reply_num
        self.save_num = save_num

    def __repr__(self) -> str:
        """Return a string representation of the request."""

        return f"<Request {self.id}>"

    # genrated by copilot
    def to_dict(self):
        """Return a JSON format of the request."""

        return {
            "id": self.id,
            "author_id": self.author_id,
            "title": self.title,
            "content": self.content,
            "community": self.community,
            "category": self.category,
            "view_num": self.view_num,
            "like_num": self.like_num,
            "reply_num": self.reply_num,
            "save_num": self.save_num,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }
