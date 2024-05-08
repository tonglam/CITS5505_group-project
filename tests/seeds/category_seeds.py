"""This module seeds the database with initial category data for testing. """

from app.extensions import db
from app.models.category import Category


def create_seed_category_data() -> list:
    """Create seed community data."""

    return [
        {"name": "movie"},
        {"name": "sports"},
        {"name": "music"},
        {"name": "food"},
        {"name": "travel"},
        {"name": "technology"},
        {"name": "education"},
        {"name": "health"},
        {"name": "fashion"},
        {"name": "art"},
        {"name": "science"},
        {"name": "business"},
        {"name": "history"},
        {"name": "nature"},
        {"name": "photography"},
        {"name": "cooking"},
        {"name": "gardening"},
        {"name": "football"},
        {"name": "culture"},
        {"name": "literature"},
    ]


def seed_category():
    """Seed the database with initial category data."""

    seed_category_data = create_seed_category_data()
    if not seed_category_data:
        return

    for data in seed_category_data:
        category = Category(
            name=data["name"],
        )
        db.session.add(category)

    db.session.commit()
