"""Test configuration file."""

# Reference: TotallyNotChase flask-unittest[https://github.com/TotallyNotChase/flask-unittest]

import os
from typing import Iterator

import flask_unittest
from bs4 import BeautifulSoup
from flask import Flask
from flask.testing import FlaskClient
from flask.wrappers import Response as TestResponse

from app import create_app
from app.extensions import db
from tests.seeds.category_seeds import seed_category
from tests.seeds.community_seeds import seed_community
from tests.seeds.notice_seeds import seed_notice
from tests.seeds.reply_seeds import seed_reply
from tests.seeds.request_seeds import seed_request
from tests.seeds.tag_seeds import seed_tag
from tests.seeds.trending_seeds import seed_trending
from tests.seeds.user_preference_seeds import seed_user_preference
from tests.seeds.user_record_seeds import seed_user_record
from tests.seeds.user_seeds import seed_user

os.environ["FLASK_ENV"] = "test"


# pylint: disable=unused-argument
def _create_app(_) -> Iterator[Flask]:
    """Create and configure a new app instance for each test."""

    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    with app.app_context():
        db.create_all()

    yield app


class TestBase(flask_unittest.AppClientTestCase):
    """Base test case for the application."""

    create_app = _create_app

    def setUp(self, app: Flask, _):
        """Set up the test case."""

        print("\nTestBase: Setting up test case.")

        with app.app_context():
            seed_user()
            seed_category()
            seed_tag()
            seed_community()
            seed_request()
            seed_reply()
            seed_user_record()
            seed_user_preference()
            seed_notice()
            seed_trending()

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

    def login(
        self,
        email: str = "test@gmail.com",
        password: str = "Password@123",
        follow_redirects: bool = True,
    ) -> None:
        """Log a user in."""

        return self._client.post(
            "/auth/login",
            data={
                "email": email,
                "password": password,
            },
            follow_redirects=follow_redirects,
        )

    def logout(self) -> None:
        """Log a user out."""

        return self._client.get("/auth/logout")


class Utils:
    """Helper class for utility functions."""

    @staticmethod
    def get_csrf_token(client: FlaskClient) -> str:
        """Get the CSRF token from the client."""

        response = client.get("/auth/login")
        csrf_token = response.html.find("input", {"name": "csrf_token"})["value"]
        return csrf_token

    @staticmethod
    def get_page_title(response: TestResponse, url: str) -> str:
        """Get the page title from the client response."""

        soup = BeautifulSoup(response.data, "html.parser")
        page_title = soup.title.text.strip() if soup.title else "No title found"
        page_title = page_title.split(" - ")[0]
        print("page_title:", page_title)
        return page_title
