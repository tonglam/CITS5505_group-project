"""This module seeds the database with initial community data for testing. """

import random

from faker import Faker

from app.extensions import db
from app.models.category import Category
from app.models.community import Community
from app.models.user import User

random.seed(5505)
faker = Faker()


def create_seed_community_data(length: int = 100) -> list:
    """Create seed community data."""

    communities = []

    category_ids = [category.id for category in Category.query.all()]
    creator_ids = [user.id for user in User.query.all()]
    names = generate_community_names(length)

    for i in range(length):
        communities.append(
            {
                "name": names[i],
                "category_id": random.choice(category_ids),
                "description": faker.text(),
                "avatar_url": "",
                "creator_id": random.choice(creator_ids),
            }
        )

    return communities


def generate_community_names(length: int) -> list:
    """Generate community names."""

    names = set()

    while len(names) < length:
        names.add(faker.name())

    return list(names)


def seed_community():
    """Seed the database with initial community data."""

    seed_community_data = create_seed_community_data()
    if not seed_community_data:
        return

    for data in seed_community_data:
        community = Community(
            name=data["name"],
            category_id=data["category_id"],
            description=data["description"],
            avatar_url=data["avatar_url"],
            creator_id=data["creator_id"],
        )
        db.session.add(community)

    db.session.commit()
