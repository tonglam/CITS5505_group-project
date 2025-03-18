"""Tests for the user module."""

from flask.testing import FlaskClient

from app.constants import HttpRequestEnum
from tests.config import AuthActions, TestBase


class TestUser(TestBase):
    """This class contains the test cases for the user module."""

    def test_get_user(self, _, client: FlaskClient):
        """Test user page."""

        url = "/users/"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_lists(self, _, client: FlaskClient):
        """Test user lists page."""

        url = "/users/lists"
        names = ["Posts", "Likes", "History", "Collects"]

        # login
        AuthActions(client).login()

        # smoke test
        for name in names:
            response = client.get(f"{url}?name={name}", follow_redirects=True)
            self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_profile(self, _, client: FlaskClient):
        """Test user profile page."""

        url = "/users/profile"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_password(self, _, client: FlaskClient):
        """Test user password page."""

        url = "/users/password"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_info(self, _, client: FlaskClient):
        """Test user info page."""

        url = "/users/info"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_notification(self, _, client: FlaskClient):
        """Test user notification page."""

        url = "/users/notification"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()
