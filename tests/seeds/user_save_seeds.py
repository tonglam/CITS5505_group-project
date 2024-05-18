"""This module seeds the database with initial user save data for testing. """

import random

from app.extensions import db
from app.models.request import Request
from app.models.reply import Reply
from app.models.user import User
from app.models.user_save import UserSave

random.seed(5505)


def create_seed_user_save_data() -> list:
    """Create seed user save data."""

    users = [user.id for user in User.query.all()]
    requests = [request.id for request in Request.query.all()]
    replies = [reply.id for reply in Reply.query.all()]

    return [
        {
            "user_id": random.choice(users),
            "request_id": random.choice(requests),
            "reply_id": random.choice(replies)
        }
        for _ in range(100)
    ]


def seed_user_save():
    """Seed the database with initial user save data."""

    seed_user_save_data = create_seed_user_save_data()
    if not seed_user_save_data:
        return

    for data in seed_user_save_data:
        user_save = UserSave(
            user_id=data["user_id"],
            request_id=data["request_id"],
            reply_id=data["reply_id"]
        )
        db.session.add(user_save)

    db.session.commit()
