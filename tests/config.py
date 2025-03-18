"""Test configuration file."""

# Reference: TotallyNotChase flask-unittest[https://github.com/TotallyNotChase/flask-unittest]

import os
from typing import Any, Dict

import flask_unittest
from bs4 import BeautifulSoup
from flask import Flask
from flask.testing import FlaskClient
from flask.wrappers import Response as TestResponse

from app import create_app
from app.extensions import db
from tests.seeds.category_seeds import seed_category
from tests.seeds.community_seeds import seed_community
from tests.seeds.reply_seeds import seed_reply
from tests.seeds.request_seeds import seed_request
from tests.seeds.tag_seeds import seed_tag
from tests.seeds.trending_seeds import seed_trending
from tests.seeds.user_like_seeds import seed_user_like
from tests.seeds.user_notice_seeds import seed_user_notice
from tests.seeds.user_preference_seeds import seed_user_preference
from tests.seeds.user_record_seeds import seed_user_record
from tests.seeds.user_save_seeds import seed_user_save
from tests.seeds.user_seeds import seed_user

os.environ["FLASK_ENV"] = "test"


def get_test_config() -> Dict[str, Any]:
    """Get test configuration."""

    return {
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "SECRET_KEY": "test-secret-key",  # Add secret key for session management
    }


def create_test_app() -> Flask:
    """Create test application."""

    app = create_app(get_test_config())
    return app


def create_test_database(app: Flask) -> None:
    """Create the test database."""

    with app.app_context():
        db.create_all()


def execute_seed_functions(app: Flask) -> None:
    """Execute seed functions to populate the test database."""

    with app.app_context():
        seed_user()
        seed_category()
        seed_tag()
        seed_community()
        seed_request()
        seed_reply()
        seed_user_record()
        seed_user_preference()
        seed_user_notice()
        seed_trending()
        seed_user_like()
        seed_user_save()


def clean_up_test_database(app: Flask) -> None:
    """Clean up the test database."""
    try:
        with app.app_context():
            db.drop_all()
    except (db.SQLAlchemyError, db.DatabaseError) as e:
        print(f"Warning: Failed to clean up test database: {e}")


class TestBase(flask_unittest.AppClientTestCase):
    """Base test case for the application."""

    def create_app(self):
        """Create test application."""
        return create_test_app()

    def setUp(self, app: Flask, _):
        """Set up the test case."""

        print("\nTestBase: Setting up test case.")
        clean_up_test_database(app)  # Clean up first
        create_test_database(app)  # Then create tables
        execute_seed_functions(app)

    def tearDown(self, app: Flask, _):
        """Tear down the test case."""

        print("\nTestBase: Tearing down test case.")
        clean_up_test_database(app)


class AuthActions:
    """Helper class for authentication actions."""

    def __init__(self, client: FlaskClient):
        """Initialize the class."""
        self._client = client
        self._access_token = None
        self._csrf_access_token = None
        self._refresh_token = None
        self._csrf_refresh_token = None

    def login(
        self,
        email: str = "test@test.com",
        password: str = "Password@123",
        follow_redirects: bool = False,
    ) -> TestResponse:
        """Login with the given credentials."""

        response = self._client.post(
            "/auth/login",
            data={"email": email, "password": password},
            follow_redirects=follow_redirects,
        )

        # Extract tokens from cookies
        cookies = response.headers.getlist("Set-Cookie")
        for cookie in cookies:
            if "access_token_cookie" in cookie:
                self._access_token = cookie.split(";")[0].split("=")[1]
            elif "csrf_access_token" in cookie:
                self._csrf_access_token = cookie.split(";")[0].split("=")[1]
            elif "refresh_token_cookie" in cookie:
                self._refresh_token = cookie.split(";")[0].split("=")[1]
            elif "csrf_refresh_token" in cookie:
                self._csrf_refresh_token = cookie.split(";")[0].split("=")[1]

        return response

    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers."""

        headers = {"Content-Type": "application/json"}

        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"

        if self._csrf_access_token:
            headers["X-CSRF-TOKEN"] = self._csrf_access_token

        return headers

    def logout(self) -> None:
        """Logout the current user."""

        self._client.get("/auth/logout")
        self._access_token = None
        self._csrf_access_token = None
        self._refresh_token = None
        self._csrf_refresh_token = None


class Utils:
    """Helper class for utility functions."""

    @staticmethod
    def get_csrf_token(client: FlaskClient) -> str:
        """Get the CSRF token from the client."""

        response = client.get("/auth/login")
        csrf_token = response.html.find("input", {"name": "csrf_token"})["value"]
        return csrf_token

    @staticmethod
    def get_page_title(response: TestResponse, _: str) -> str:
        """Get the page title from the client response."""

        soup = BeautifulSoup(response.data, "html.parser")
        page_title = soup.title.text.strip() if soup.title else "No title found"
        page_title = page_title.split(" - ")[0]
        return page_title
