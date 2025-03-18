"""User job."""

import random
import string

from faker import Faker
from flask_apscheduler import APScheduler
from sqlalchemy.exc import SQLAlchemyError

from app.constants import (
    JOB_INTERVAL,
    USER_LIKE_MAX_NUM,
    USER_MAX_NUM,
    USER_RECORD_MAX_NUM,
    USER_SAVE_MAX_NUM,
)
from app.extensions import db
from app.models.community import Community
from app.models.reply import Reply
from app.models.request import Request
from app.models.user import User
from app.models.user_like import UserLike
from app.models.user_preference import UserPreference
from app.models.user_record import UserRecord
from app.models.user_save import UserSave

faker = Faker()
random.seed(5505)

scheduler = APScheduler()


def init_scheduler(app):
    """Initialize the scheduler."""
    scheduler.init_app(app)
    scheduler.start()


@scheduler.task(
    "interval",
    id="create_user",
    seconds=JOB_INTERVAL.get("create_user"),
    misfire_grace_time=900,  # Allow 15 minutes grace time
    max_instances=1,  # Prevent multiple instances
)
def create_user_job():
    """Create user job."""
    try:
        # Skip if maximum users reached
        with scheduler.app.app_context():
            if User.query.count() >= USER_MAX_NUM:
                return

        scheduler.app.logger.info("Start [create_user_job]...")
        create_user()
        scheduler.app.logger.info("End [create_user_job]...")
    except SQLAlchemyError as e:
        scheduler.app.logger.error(f"Error [create_user_job]: {str(e)}")


def create_user():
    """Create a new user."""
    with scheduler.app.app_context():
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
        db.session.flush()  # Get user.id without committing

        communities = Community.query.with_entities(Community.id).all()
        user_communities = random.choices(
            [c[0] for c in communities], k=random.randint(1, 5)
        )

        user_preference = UserPreference(
            user_id=user.id,
            communities=str(user_communities),
        )
        db.session.add(user_preference)
        db.session.commit()


def generate_test_email(domain="gmail.com", length=10):
    """Generate a test email."""
    username = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    return f"{username}@{domain}"


@scheduler.task(
    "interval",
    id="create_user_record",
    seconds=JOB_INTERVAL.get("create_user_record"),
    misfire_grace_time=300,
    max_instances=1,
)
def create_user_record_job():
    """Create user record job."""
    try:
        # Skip if maximum records reached
        with scheduler.app.app_context():
            if UserRecord.query.count() >= USER_RECORD_MAX_NUM:
                return

        scheduler.app.logger.info("Start [create_user_record_job]...")
        create_user_record()
        scheduler.app.logger.info("End [create_user_record_job]...")
    except SQLAlchemyError as e:
        scheduler.app.logger.error(f"Error [create_user_record_job]: {str(e)}")


def create_user_record():
    """Create a new user record."""
    with scheduler.app.app_context():
        # Get random user and request IDs efficiently
        user = User.query.order_by(db.func.random()).first()
        request = Request.query.order_by(db.func.random()).first()

        if not user or not request:
            return

        user_record = UserRecord(
            user_id=user.id,
            request_id=request.id,
        )

        db.session.add(user_record)
        db.session.commit()


@scheduler.task(
    "interval",
    id="create_user_like",
    seconds=JOB_INTERVAL.get("create_user_like"),
    misfire_grace_time=300,
    max_instances=1,
)
def create_user_like_job():
    """Create user like job."""
    try:
        # Skip if maximum likes reached
        with scheduler.app.app_context():
            if UserLike.query.count() >= USER_LIKE_MAX_NUM:
                return

        scheduler.app.logger.info("Start [create_user_like_job]...")
        create_user_like()
        scheduler.app.logger.info("End [create_user_like_job]...")
    except SQLAlchemyError as e:
        scheduler.app.logger.error(f"Error [create_user_like_job]: {str(e)}")


def create_user_like():
    """Create a new user like."""
    with scheduler.app.app_context():
        # Get random records efficiently
        user = User.query.order_by(db.func.random()).first()
        request = Request.query.order_by(db.func.random()).first()
        reply = Reply.query.order_by(db.func.random()).first()

        if not user or not request or not reply:
            return

        user_like = UserLike(
            user_id=user.id,
            request_id=request.id,
            reply_id=reply.id,
        )

        db.session.add(user_like)
        db.session.commit()


@scheduler.task(
    "interval",
    id="create_user_save",
    seconds=JOB_INTERVAL.get("create_user_save"),
    misfire_grace_time=300,
    max_instances=1,
)
def create_user_save_job():
    """Create user save job."""
    try:
        # Skip if maximum saves reached
        with scheduler.app.app_context():
            if UserSave.query.count() >= USER_SAVE_MAX_NUM:
                return

        scheduler.app.logger.info("Start [create_user_save_job]...")
        create_user_save()
        scheduler.app.logger.info("End [create_user_save_job]...")
    except SQLAlchemyError as e:
        scheduler.app.logger.error(f"Error [create_user_save_job]: {str(e)}")


def create_user_save():
    """Create a new user save."""
    with scheduler.app.app_context():
        # Get random records efficiently
        user = User.query.order_by(db.func.random()).first()
        request = Request.query.order_by(db.func.random()).first()
        reply = Reply.query.order_by(db.func.random()).first()

        if not user or not request or not reply:
            return

        user_save = UserSave(
            user_id=user.id,
            request_id=request.id,
            reply_id=reply.id,
        )

        db.session.add(user_save)
        db.session.commit()
