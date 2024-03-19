"""User model."""

import datetime

from sqlalchemy import event

from app.extensions import bcrypt, db
from app.utils import generate_time, generate_uuid


# pylint: disable=too-few-public-methods
class User(db.Model):
    """User model."""

    user_id: str = db.Column(db.String(36), primary_key=True, default=generate_uuid())
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password: str = db.Column(db.String(300), nullable=True)
    avatar_url: str = db.Column(db.String(300), default="")
    authenticated: bool = db.Column(db.Boolean, default=False)
    use_google: bool = db.Column(db.Boolean, default=False)
    use_github: bool = db.Column(db.Boolean, default=False)
    create_at: datetime = db.Column(db.DateTime, default=generate_time())
    update_at: datetime = db.Column(db.DateTime, default=generate_time())

    def __init__(
        self,
        username: str,
        email: str,
        password: str = "",
        avatar_url: str = "",
        authenticated: bool = False,
        use_google: bool = False,
        use_github: bool = False,
    ) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.avatar_url = avatar_url
        self.authenticated = authenticated
        self.use_google = use_google
        self.use_github = use_github

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def check_password(self, password: str) -> bool:
        """Check the password."""

        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self) -> bool:
        """Check if the user is authenticated."""

        return self.authenticated

    def is_active(self) -> bool:
        """Check if the user is active."""

        return True

    def is_anonymous(self) -> bool:
        """Check if the user is anonymous."""

        return False

    def get_id(self) -> str:
        """Get the user id."""

        return self.user_id


# pylint: disable=unused-argument
@event.listens_for(User, "before_insert")
def before_insert_listener(mapper, connect, target):
    """Update the create time before inserting a new user."""

    target.userId = generate_uuid()
    if target.password:
        target.password = bcrypt.generate_password_hash(target.password).decode("utf-8")
    target.createTime = generate_time()
    target.updateTime = generate_time()


@event.listens_for(User, "before_update")
def before_update_listener(mapper, connect, target):
    """Update the update time before updating a user."""

    target.updateTime = generate_time()
