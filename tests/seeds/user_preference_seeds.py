"""This module seeds the database with initial user preference data for testing. """

import random

from app.extensions import db
from app.models.category import Category
from app.models.community import Community
from app.models.user import User
from app.models.user_preference import UserPreference

random.seed(5505)


def create_seed_user_preference_data() -> list:
    """Create seed user preference data."""

    users = [user.id for user in User.query.all()]
    communities = [community.id for community in Community.query.all()]
    categories = [category.id for category in Category.query.all()]

    return [
        {
            "user_id": users[i],
            "communities": create_communities(communities),
            "interests": create_interests(categories),
        }
        for i in range(len(users))
    ]


def create_communities(communities: list) -> str:
    """Create a string of communities for user preference."""

    community_datas = []
    for _ in range(random.randint(1, 5)):
        community_datas.append(random.choice(communities))

    return str(community_datas)


def create_interests(categories: list) -> str:
    """Create a string of interests for user preference."""

    interest_datas = []
    for _ in range(random.randint(1, 5)):
        interest_datas.append(random.choice(categories))

    return str(interest_datas)


def seed_user_preference():
    """Seed the database with initial user preference data."""

    seed_user_preference_data = create_seed_user_preference_data()
    if not seed_user_preference_data:
        return

    for data in seed_user_preference_data:
        user_preference = UserPreference(
            user_id=data["user_id"],
            communities=data["communities"],
            interests=data["interests"],
        )
        db.session.add(user_preference)

    db.session.commit()
