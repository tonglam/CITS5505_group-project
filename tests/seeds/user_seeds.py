"""This module seeds the database with initial user data for testing. """

from app.extensions import db
from app.models import User

seed_user_data: list = [
    {
        "username": "test_user1",
        "email": "test_user1@example.com",
        "avatar_url": "https://gravatar.com/avatar/987b26ec2720f3e91a8a61ea2149b247?s=400&d=robohash&r=x",
        "password": "Password@123",
        "security_question": "What is your favorite color?",
        "security_answer": "blue",
    },
    {
        "username": "test_user2",
        "email": "test_user2@example.com",
        "avatar_url": "https://gravatar.com/avatar/9547e218666ce51c3cc3352c09a5ae22?s=400&d=robohash&r=x",
        "password": "Password@123",
        "security_question": "What is your favorite food?",
        "security_answer": "pizza",
    },
]


def seed_users():
    """Seed the database with initial user data."""

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


if __name__ == "__main__":
    seed_users()
