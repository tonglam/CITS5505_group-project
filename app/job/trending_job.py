"""Trending job."""

import random

from faker import Faker
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from app.constants import JOB_INTERVAL
from app.extensions import db, scheduler
from app.models.request import Request
from app.models.trending import Trending
from app.models.user_record import UserRecord

faker = Faker()
random.seed(5505)


@scheduler.task(
    "interval", id="update_trending_job", seconds=JOB_INTERVAL.get("update_trending")
)
def update_trending_job():
    """Update trending job."""

    try:
        scheduler.app.logger.info("Start [update_trending_job]...")
        update_trending()
        scheduler.app.logger.info("End [update_trending_job]...")
    except SQLAlchemyError as e:
        scheduler.app.logger.error(f"Error [update_trending_job]: {str(e)}")


def update_trending():
    """Update trending."""

    with scheduler.app.app_context():
        # delete trending table
        Trending.query.delete()
        db.session.commit()

        # top 100 viewed requests
        # pylint: disable=not-callable
        top_user_records = (
            db.session.query(
                UserRecord.request_id,
                func.count(UserRecord.request_id).label("view_count"),
            )
            .group_by(UserRecord.request_id)
            .order_by(func.count(UserRecord.request_id).desc())
            .limit(100)
            .all()
        )

        for user_record in top_user_records:
            request_id = user_record.request_id
            view_count = user_record.view_count

            request = Request.query.get(request_id)
            if not request:
                continue

            trending = Trending(
                request_id, request.author_id, view_count, request.reply_num
            )
            db.session.add(trending)

        db.session.commit()

        scheduler.app.logger.info(
            "Trending updated successfully from [update_trending_job]."
        )
