"""This module seeds the database with initial user notice data for testing. """

import random

from app.extensions import db
from app.models.user import User
from app.models.user_notice import (
    UserNotice,
    UserNoticeActionEnum,
    UserNoticeModuleEnum,
)

random.seed(5505)


def create_seed_user_notice_data() -> list:
    """Create seed user notice data."""

    user_notifications = []

    users = [user.id for user in User.query.all()]
    user_modules = [module.value for module in UserNoticeModuleEnum]
    user_actions = [action.value for action in UserNoticeActionEnum]

    for _ in range(20):
        user_id = random.choice(users)
        user_notice_action = random.choice(user_actions)

        for module in user_modules:
            user_notifications.append(
                {
                    "user_id": user_id,
                    "subject": f"Notification: {module}",
                    "content": f"{user_notice_action} successfully!",
                    "module": module,
                    "status": random.choice([True, False]),
                }
            )

    return user_notifications


def seed_user_notice():
    """Seed the database with initial user notice data."""

    seed_user_notice_data = create_seed_user_notice_data()
    if not seed_user_notice_data:
        return

    for data in seed_user_notice_data:
        notice = UserNotice(
            user_id=data["user_id"],
            subject=data["subject"],
            content=data["content"],
            module=data["module"],
            status=data["status"],
        )
        db.session.add(notice)

    db.session.commit()
