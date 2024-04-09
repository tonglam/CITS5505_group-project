"""Test configuration file."""

# Reference: TotallyNotChase flask-unittest[https://github.com/TotallyNotChase/flask-unittest]

import os
from typing import Iterator

import flask_unittest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.extensions import db
from tests.seeds.user_seeds import seed_users

os.environ["FLASK_ENV"] = "test"


# pylint: disable=unused-argument
def _create_app(_) -> Iterator[Flask]:
    """Create and configure a new app instance for each test."""

    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()

    yield app


class TestBase(flask_unittest.AppClientTestCase):
    """Base test case for the application."""

    create_app = _create_app

    def setUp(self, app: Flask, _):
        """Set up the test case."""

        print("\nTestBase: Setting up test case.")
        # insert test data seed for all tests
        with app.app_context():
            seed_users()

    def tearDown(self, app: Flask, _):
        """Tear down the test case."""

        print("\nTestBase: Tearing down test case.")
        # clean up test database
        with app.app_context():
            db.drop_all()


class AuthActions:
    """Helper class for handling authentication."""

    def __init__(self, client: FlaskClient):
        self._client = client

    def login(self, email: str, password: str):
        """Log a user in."""
        return self._client.post(
            "/login",
            data={
                "email": email,
                "password": password,
            },
        )

    def logout(self) -> FlaskClient:
        """Log a user out."""
        return self._client.get("/logout")