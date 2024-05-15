"""User job."""

import random
import string

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from app.constants import (
    JOB_INTERVAL,
    USER_LIKE_MAX_NUM,
    USER_MAX_NUM,
    USER_RECORD_MAX_NUM,
    USER_SAVE_MAX_NUM,
)
from app.extensions import db, scheduler
from app.models.community import Community
from app.models.request import Request
from app.models.user import User
from app.models.user_like import UserLike
from app.models.user_preference import UserPreference
from app.models.user_record import UserRecord
from app.models.user_save import UserSave

faker = Faker()
random.seed(5505)


@scheduler.task("interval", id="create_user", seconds=JOB_INTERVAL.get("create_user"))
def create_user_job():
    """Create a new user job."""

    try:
        scheduler.app.logger.info("Start [create_user_job]...")
        create_user()
        scheduler.app.logger.info("End [create_user_job]...")
    except SQLAlchemyError as e:
        scheduler.app.logger.error(f"Error [create_user_job]: {str(e)}")


def create_user():
    """Create a new user."""

    with scheduler.app.app_context():
        if User.query.count() >= USER_MAX_NUM:
            scheduler.app.logger.info("User reached the maximum number.")
            return

        username = faker.name()

        user = User(
            username=username,
            email=generate_test_email(),
            avatar_url=f"https://api.dicebear.com/5.x/adventurer/svg?seed={username}",
            use_google=False,
            use_github=False,
            security_question=faker.sentence(),
            security_answer=faker.word(),
        )

        db.session.add(user)

        communities = [community.id for community in Community.query.all()]
        user_communities = random.choices(communities, k=random.randint(1, 5))

        user_preference = UserPreference(
            user_id=user.id,
            communities=user_communities,
        )
        db.session.add(user_preference)

        db.session.commit()

        scheduler.app.logger.info(
            "Community created successfully from [create_user_job]."
        )


def generate_test_email(domain="gmail.com", length=10):
    """Generate a test email."""

    username = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    return f"{username}@{domain}"


@scheduler.task(
    "interval",
    id="create_user_record_job",
    seconds=JOB_INTERVAL.get("create_user_record"),
)
def create_user_record_job():
    """Create a new user record job."""

    try:
        scheduler.app.logger.info("Start [create_user_record_job]...")
        create_user_record()
        scheduler.app.logger.info("End [create_user_record_job]...")
    except SQLAlchemyError as e:
        scheduler.app.logger.error(f"Error [create_user_record_job]: {str(e)}")


def create_user_record():
    """Create a new user record."""

    with scheduler.app.app_context():
        if User.query.count() >= USER_RECORD_MAX_NUM:
            scheduler.app.logger.info("User Record reached the maximum number.")
            return

        users = [user.id for user in User.query.all()]
        requests = [request.id for request in Request.query.all()]

        user_record = UserRecord(
            user_id=random.choice(users),
            request_id=random.choice(requests),
        )

        db.session.add(user_record)
        db.session.commit()

        scheduler.app.logger.info(
            "User Record created successfully from [create_user_record_job]."
        )


@scheduler.task(
    "interval", id="create_user_like", seconds=JOB_INTERVAL.get("create_user_like")
)
def create_user_like_job():
    """Create a new user like job."""

    try:
        scheduler.app.logger.info("Start [create_user_like_job]...")
        create_user_like()
        scheduler.app.logger.info("End [create_user_like_job]...")
    except SQLAlchemyError as e:
        scheduler.app.logger.error(f"Error [create_user_like_job]: {str(e)}")


def create_user_like():
    """Create a new user like."""

    with scheduler.app.app_context():
        if User.query.count() >= USER_LIKE_MAX_NUM:
            scheduler.app.logger.info("User like reached the maximum number.")
            return

        users = [user.id for user in User.query.all()]
        requests = [request.id for request in Request.query.all()]

        user_like = UserLike(
            user_id=random.choice(users),
            request_id=random.choice(requests),
        )

        db.session.add(user_like)
        db.session.commit()

        scheduler.app.logger.info(
            "User Like created successfully from [create_user_like_job]."
        )


@scheduler.task(
    "interval", id="create_user_save", seconds=JOB_INTERVAL.get("create_user_save")
)
def create_user_save_job():
    """Create a new user save job."""

    try:
        scheduler.app.logger.info("Start [create_user_save_job]...")
        create_user_save()
        scheduler.app.logger.info("End [create_user_save_job]...")
    except SQLAlchemyError as e:
        scheduler.app.logger.error(f"Error [create_user_save_job]: {str(e)}")


def create_user_save():
    """Create a new user save."""

    with scheduler.app.app_context():
        if User.query.count() >= USER_SAVE_MAX_NUM:
            scheduler.app.logger.info("User save reached the maximum number.")
            return

        users = [user.id for user in User.query.all()]
        requests = [request.id for request in Request.query.all()]

        user_save = UserSave(
            user_id=random.choice(users),
            request_id=random.choice(requests),
        )

        db.session.add(user_save)
        db.session.commit()

        scheduler.app.logger.info(
            "User Save created successfully from [create_user_save_job]."
        )
