"""Tests for the popular module."""

from flask.testing import FlaskClient

from app.constants import HttpRequestEnum
from tests.config import AuthActions, TestBase


class TestPopular(TestBase):
    """This class contains the test cases for the popular module."""

    def test_popular(self, _, client: FlaskClient):
        """Test the popular method."""
        url = "/populars/"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()
