"""This module seeds the database with initial notice data for testing. """

import random

from app.extensions import db
from app.models.notice import Notice, NoticeActionEnum, NoticeModuleEnum
from app.models.user import User

random.seed(5505)


def create_seed_notice_data() -> list:
    """Create seed notice data."""

    notifications = []

    users = [user.id for user in User.query.all()]
    modules = [module.value for module in NoticeModuleEnum]
    actions = [action.value for action in NoticeActionEnum]

    for _ in range(20):
        user_id = random.choice(users)
        notice_action = random.choice(actions)

        for module in modules:
            notifications.append(
                {
                    "user_id": user_id,
                    "subject": f"Notification: {module}",
                    "content": f"{notice_action} successfully!",
                    "module": module,
                    "status": random.choice([True, False]),
                }
            )

    return notifications


def seed_notice():
    """Seed the database with initial notice data."""

    seed_notice_data = create_seed_notice_data()
    if not seed_notice_data:
        return

    for data in seed_notice_data:
        notice = Notice(
            user_id=data["user_id"],
            subject=data["subject"],
            content=data["content"],
            module=data["module"],
            status=data["status"],
        )
        db.session.add(notice)

    db.session.commit()
