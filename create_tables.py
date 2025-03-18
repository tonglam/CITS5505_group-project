"""Create database tables from models."""

from app import create_app
from app.extensions import db
from app.models import (
    Category,
    Community,
    Reply,
    Request,
    Tag,
    Trending,
    User,
    UserLike,
    UserNotice,
    UserPreference,
    UserRecord,
    UserSave,
)

app = create_app()
with app.app_context():
    # Create all tables
    db.create_all()
    print("All tables created successfully!")
