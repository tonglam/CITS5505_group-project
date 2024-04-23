"""This module seeds the database with initial user record data for testing. """

import random

from app.extensions import db
from app.models.request import Request
from app.models.user import User
from app.models.user_record import UserRecord, UserRecordEnum

random.seed(5505)


def create_seed_user_record_data() -> list:
    """Create seed user record data."""

    users = [user.id for user in User.query.all()]
    communities = [request.id for request in Request.query.all()]
    types = [record_type.value for record_type in UserRecordEnum]

    return [
        {
            "user_id": random.choice(users),
            "request_id": random.choice(communities),
            "record_type": random.choice(types),
        }
        for _ in range(100)
    ]


def seed_user_record():
    """Seed the database with initial user record data."""

    seed_user_record_data = create_seed_user_record_data()
    if not seed_user_record_data:
        return

    for data in seed_user_record_data:
        user_record = UserRecord(
            user_id=data["user_id"],
            request_id=data["request_id"],
            record_type=data["record_type"],
        )
        db.session.add(user_record)

    db.session.commit()
