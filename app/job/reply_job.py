"""Reply job."""

import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from app.constants import JOB_INTERVAL, REPLY_MAX_NUM
from app.extensions import db, scheduler
from app.models.reply import Reply, ReplySourceEnum
from app.models.request import Request
from app.models.user import User

faker = Faker()
random.seed(5505)


@scheduler.task(
    "interval", id="create_reply_job", seconds=JOB_INTERVAL.get("create_reply")
)
def create_reply_job():
    """Create a new reply job."""

    try:
        scheduler.app.logger.info("Start [create_reply_job]...")
        create_reply()
        scheduler.app.logger.info("End [create_reply_job]...")
    except SQLAlchemyError as e:
        scheduler.app.logger.error(f"Error [create_reply_job]: {str(e)}")


def create_reply():
    """Create a new reply."""

    with scheduler.app.app_context():
        if Reply.query.count() >= REPLY_MAX_NUM:
            scheduler.app.logger.info("Reply reached the maximum number.")
            return

        requests = [request.id for request in Request.query.all()]
        users = [user.id for user in User.query.all()]
        request_id = random.choice(requests)

        request = Reply(
            request_id=request_id,
            replier_id=random.choice(users),
            reply_id=request_id,
            content=faker.text(),
            source=ReplySourceEnum.AI.value,
            like_num=random.randint(0, 10000),
            save_num=random.randint(0, 10000),
        )

        db.session.add(request)
        db.session.commit()

        scheduler.app.logger.info("Reply created successfully from [create_reply_job].")
