"""Test configuration file."""

# Reference: TotallyNotChase flask-unittest[https://github.com/TotallyNotChase/flask-unittest]

import os
from typing import Any, Dict, Iterator, Union

import flask_unittest
from bs4 import BeautifulSoup
from flask import Flask
from flask.testing import FlaskClient
from flask.wrappers import Response as TestResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy.sql import text
from webdriver_manager.chrome import ChromeDriverManager

from app import create_app
from app.extensions import db
from app.utils import get_config
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
        "SQLALCHEMY_DATABASE_URI": get_config("POSTGRESQL", "DATABASE_URL") + "_test",
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

    with app.app_context():
        db.drop_all()


class TestBase(flask_unittest.AppClientTestCase):
    """Base test case for the application."""

    create_app = create_test_app

    def setUp(self, app: Flask, _):
        """Set up the test case."""

        print("\nTestBase: Setting up test case.")
        execute_seed_functions(app)

    def tearDown(self, app: Flask, _):
        """Tear down the test case."""

        print("\nTestBase: Tearing down test case.")
        clean_up_test_database(app)


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
        return page_title


class SeleniumTestBase:
    """Base class for Selenium tests."""

    def setUp(self) -> None:
        """Set up test case."""

        self.app = create_test_app()
        self.client = self.app.test_client()

        # set up chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # set up chrome driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # set up wait time
        self.driver.implicitly_wait(10)

    def tearDown(self) -> None:
        """Tear down test case."""

        self.driver.quit()


class TestSeleniumSetup(SeleniumTestBase):
    """This class contains the setup test case."""

    def test_setup(self):
        """Test the setup of the Selenium test case."""

        create_test_database(self.app)
        execute_seed_functions(self.app)
        clean_up_test_database(self.app)


class TestSeleniumCleanup(SeleniumTestBase):
    """This class contains the cleanup test case."""

    def test_cleanup(self):
        """Test the cleanup of the Selenium test case."""

        clean_up_test_database(self.app)
