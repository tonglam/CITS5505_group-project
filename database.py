"""Database module."""

from app import create_app
from app.extensions import db, msearch

app = create_app()


def create_db() -> None:
    """Create the database."""

    with app.app_context():
        db.drop_all()
        db.create_all()
        msearch.create_index(update=True)


if __name__ == "__main__":
    create_db()
