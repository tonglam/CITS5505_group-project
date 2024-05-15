"""Request job."""

import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from app.constants import JOB_INTERVAL, REQUEST_MAX_NUM
from app.extensions import db, scheduler
from app.models.category import Category
from app.models.community import Community
from app.models.request import Request
from app.models.user import User

faker = Faker()
random.seed(5505)


@scheduler.task(
    "interval", id="create_request_job", seconds=JOB_INTERVAL.get("create_request")
)
def create_request_job():
    """Create a new request job."""

    try:
        scheduler.app.logger.info("Start [create_request_job]...")
        create_request()
        scheduler.app.logger.info("End [create_request_job]...")
    except SQLAlchemyError as e:
        # skip db constraint validations, so may occur Error sometimes
        scheduler.app.logger.error(f"Error [create_request_job]: {str(e)}")


def create_request():
    """Create a new request."""

    with scheduler.app.app_context():
        if Request.query.count() >= REQUEST_MAX_NUM:
            scheduler.app.logger.info("Request reached the maximum number.")
            return

        users = [user.id for user in User.query.all()]
        communities = [community.id for community in Community.query.all()]
        categories = [category.id for category in Category.query.all()]

        request = Request(
            author_id=random.choice(users),
            title=faker.sentence(),
            content=faker.text(),
            community_id=random.choice(communities),
            tag_id=random.choice(categories),
            view_num=random.randint(0, 10000),
            like_num=random.randint(0, 10000),
            reply_num=random.randint(0, 10000),
            save_num=random.randint(0, 10000),
        )

        db.session.add(request)
        db.session.commit()

        scheduler.app.logger.info(
            "Request created successfully from [create_request_job]."
        )
