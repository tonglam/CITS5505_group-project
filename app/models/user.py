"""User model."""

import datetime
import hashlib

from flask_login import UserMixin
from sqlalchemy import event

from app.constant import GRAVATAR_URL, UserStatusEnum
from app.extensions import bcrypt, db
from app.utils import generate_time, generate_uuid


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class User(UserMixin, db.Model):
    """User model."""

    user_id: str = db.Column(db.String(36), primary_key=True, default=generate_uuid())
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(300), nullable=True)
    avatar_url: str = db.Column(db.String(300), default="")
    use_google: bool = db.Column(db.Boolean, default=False)
    use_github: bool = db.Column(db.Boolean, default=False)
    security_question: str = db.Column(db.String(300), nullable=True)
    security_answer: str = db.Column(db.String(300), nullable=True)
    status: str = db.Column(db.String(20), default=UserStatusEnum.ACTIVE.value)
    create_at: datetime = db.Column(db.DateTime, default=generate_time())
    update_at: datetime = db.Column(db.DateTime, default=generate_time())

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        username: str,
        email: str,
        avatar_url: str = "",
        use_google: bool = False,
        use_github: bool = False,
        security_question: str = "",
        security_answer: str = "",
    ) -> None:
        self.username = username
        self.email = email
        self.avatar_url = avatar_url
        self.use_google = use_google
        self.use_github = use_github
        self.security_question = security_question
        self.security_answer = security_answer

    @property
    def password(self) -> str:
        """Get the password hash."""
        return self.password_hash

    @password.setter
    def password(self, password: str) -> None:
        """Set password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def verify_password(self, password: str) -> bool:
        """Check the password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        """Get the user id."""
        return self.user_id

    @staticmethod
    def user_exists(email: str) -> bool:
        """Check if the user is the user."""
        return User.query.filter_by(email=email).first() is not None

    # genrated by copilot
    def to_dict(self):
        """Return a JSON format of the user."""
        return {
            "userId": self.user_id,
            "username": self.username,
            "email": self.email,
            "avatarUrl": self.avatar_url,
            "useGoogle": self.use_google,
            "useGithub": self.use_github,
            "securityQuestion": self.security_question,
            "securityAnswer": self.security_answer,
            "status": self.status,
            "createAt": self.create_at,
            "updateAt": self.update_at,
        }


# pylint: disable=unused-argument
@event.listens_for(User, "before_insert")
def before_insert_listener(mapper, connect, target):
    """Update the create time before inserting a new user."""
    target.userId = generate_uuid()
    target.avatar_url = check_avatar_url(target.avatar_url, target.email)
    print(target.avatar_url)
    target.create_at = generate_time()
    target.update_at = generate_time()


def check_avatar_url(avatar_url, email):
    """Check the avatar url."""
    if not avatar_url and email:
        return f"{GRAVATAR_URL}{hashlib.sha256(email.lower().encode()).hexdigest()}"
    return avatar_url


@event.listens_for(User, "before_update")
def before_update_listener(mapper, connect, target):
    """Update the update time before updating a user."""
    target.update_at = generate_time()
