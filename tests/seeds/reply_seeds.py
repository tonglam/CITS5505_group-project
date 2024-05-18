"""This module seeds the database with initial reply data for testing. """

import random

from faker import Faker

from app.extensions import db
from app.models.reply import Reply, ReplySourceEnum
from app.models.request import Request
from app.models.user import User

random.seed(5505)
faker = Faker()


def create_seed_reply_data() -> list:
    """Create seed reply data."""

    requests = [request.id for request in Request.query.all()]
    users = [user.id for user in User.query.all()]
    reply_sources = [source.value for source in ReplySourceEnum]

    replies = []
    for _ in range(50):  # Create initial replies to requests
        request_id = random.choice(requests)
        replies.append(
            {
                "request_id": request_id,
                "replier_id": random.choice(users),
                "reply_id": request_id,
                "content": faker.text(),
                "source": random.choice(reply_sources),
                "like_num": random.randint(0, 100),
                "save_num": random.randint(0, 100),
            }
        )

    for _ in range(50):
        parent_reply = random.choice(replies)
        replies.append(
            {
                "request_id": parent_reply["request_id"],
                "replier_id": random.choice(users),
                "reply_id": parent_reply["reply_id"],
                "content": faker.text(),
                "source": random.choice(reply_sources),
                "like_num": random.randint(0, 100),
                "save_num": random.randint(0, 100),
            }
        )

    return replies


def seed_reply():
    """Seed the database with initial reply data."""

    seed_reply_data = create_seed_reply_data()
    if not seed_reply_data:
        return

    for data in seed_reply_data:
        reply = Reply(
            request_id=data["request_id"],
            replier_id=data["replier_id"],
            reply_id=data["reply_id"],
            content=data["content"],
            source=data["source"],
            like_num=data["like_num"],
            save_num=data["save_num"],
        )
        db.session.add(reply)

    db.session.commit()
