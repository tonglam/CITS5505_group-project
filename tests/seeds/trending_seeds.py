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

    trendings = []

    requests = [request for request in Request.query.all()]
    users = [user.id for user in User.query.all()]

    for _ in range(100):
        requests = random.choice(requests)
        user_id = random.choice(users)

        trendings.append(
            {
                "request_id": requests.id,
                "title": requests.title,
                "author_id": user_id,
                "reply_num": random.randint(0, 100),
            }
        )

    return trendings


def seed_trending():
    """Seed the database with initial trending data."""

    seed_trending_data = create_seed_trending_data()
    if not seed_trending_data:
        return

    for data in seed_trending_data:
        trending = Trending(
            request_id=data["request_id"],
            title=data["title"],
            author_id=data["author_id"],
            reply_num=data["reply_num"],
        )
        db.session.add(trending)

    db.session.commit()
