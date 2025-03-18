"""This module seeds the database with initial user data for testing."""

import random
import string

from faker import Faker

from app.extensions import db
from app.models.user import User

random.seed(5505)
faker = Faker()


def create_seed_user_data() -> list:
    """Create seed user data."""

    users = [
        {
            "username": f"{faker.name()}_{i}",
            "email": generate_test_email(),
            "avatar_url": f"https://api.dicebear.com/5.x/adventurer/svg?seed={random.randint(1, 1000)}",
            "password": "Password@123",
            "security_question": "What is your favorite color?",
            "security_answer": "blue",
        }
        for i in range(10)
    ]

    users.append(
        {
            "username": "test",
            "email": "test@gmail.com",
            "avatar_url": "https://api.dicebear.com/5.x/adventurer/svg?seed=5505",
            "password": "Password@123",
            "security_question": "What is your favorite color?",
            "security_answer": "blue",
        }
    )

    return users


def generate_test_email(domain="gmail.com", length=10):
    """Generate a test email."""

    username = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    return f"{username}@{domain}"


seed_user_data = create_seed_user_data()


def seed_user():
    """Seed the database with initial user data."""

    if not seed_user_data:
        return

    for data in seed_user_data:
        user = User(
            username=data["username"],
            email=data["email"],
            avatar_url=data["avatar_url"],
            use_google=False,
            use_github=False,
            security_question=data["security_question"],
            security_answer=data["security_answer"],
        )
        user.password = data["password"]
        db.session.add(user)

    db.session.commit()
