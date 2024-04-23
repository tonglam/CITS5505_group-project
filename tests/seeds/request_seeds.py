"""This module seeds the database with initial request data for testing. """

import random

from faker import Faker

from app.extensions import db
from app.models.category import Category
from app.models.community import Community
from app.models.request import Request
from app.models.user import User

random.seed(5505)
faker = Faker()


def create_seed_request_data() -> list:
    """Create seed request data."""

    communities = [community.id for community in Community.query.all()]
    users = [user.id for user in User.query.all()]
    categories = [category.id for category in Category.query.all()]

    return [
        {
            "community": random.choice(communities),
            "author": random.choice(users),
            "title": faker.sentence(),
            "content": faker.text(),
            "category": random.choice(categories),
            "view_num": random.randint(0, 100),
            "like_num": random.randint(0, 100),
            "reply_num": random.randint(0, 100),
            "save_num": random.randint(0, 100),
        }
        for _ in range(100)
    ]


def seed_request():
    """Seed the database with initial request data."""

    seed_request_data = create_seed_request_data()
    if not seed_request_data:
        return

    for data in seed_request_data:
        request = Request(
            community=data["community"],
            author=data["author"],
            title=data["title"],
            content=data["content"],
            category=data["category"],
            view_num=data["view_num"],
            like_num=data["like_num"],
            reply_num=data["reply_num"],
            save_num=data["save_num"],
        )
        db.session.add(request)

    db.session.commit()
