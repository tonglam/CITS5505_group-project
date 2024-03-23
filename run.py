"""This file is used to run the application."""

from app import create_app
from app.extensions import scheduler

app = create_app()


if __name__ == "__main__":
    scheduler.start()
    app.run(debug=True)
