"""This module seeds the database with initial trending data for testing. """

import random

from faker import Faker

from app.extensions import db
from app.models.request import Request
from app.models.trending import Trending
from app.models.user import User

random.seed(5505)
faker = Faker()


def create_seed_trending_data() -> list:
    """Create seed trending data."""

    requests = [request.id for request in Request.query.all()]
    users = [user.id for user in User.query.all()]

    return [
        {
            "request_id": requests[i],
            "author_id": random.choice(users),
            "reply_num": random.randint(0, 100),
        }
        for i in range(len(requests))
    ]


def seed_trending():
    """Seed the database with initial trending data."""

    seed_trending_data = create_seed_trending_data()
    if not seed_trending_data:
        return

    for data in seed_trending_data:
        trending = Trending(
            request_id=data["request_id"],
            author_id=data["author_id"],
            reply_num=data["reply_num"],
        )
        db.session.add(trending)

    db.session.commit()
