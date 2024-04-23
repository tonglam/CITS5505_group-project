"""This module seeds the database with initial community data for testing. """

import random

from faker import Faker

from app.extensions import db
from app.models.category import Category
from app.models.community import Community

random.seed(5505)
faker = Faker()


def create_seed_community_data() -> list:
    """Create seed community data."""

    category_ids = [category.id for category in Category.query.all()]

    return [
        {
            "name": faker.name(),
            "category": random.choice(category_ids),
            "description": faker.text(),
            "avatar": "",
        }
        for _ in range(100)
    ]


def seed_community():
    """Seed the database with initial community data."""

    seed_community_data = create_seed_community_data()
    if not seed_community_data:
        return

    for data in seed_community_data:
        community = Community(
            name=data["name"],
            category=data["category"],
            description=data["description"],
            avatar=data["avatar"],
        )
        db.session.add(community)

    db.session.commit()
