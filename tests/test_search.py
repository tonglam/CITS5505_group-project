"""Tests for the search module."""

from flask.testing import FlaskClient

from app.constants import HttpRequestEnum
from tests.config import AuthActions, TestBase


class TestSearch(TestBase):
    """This class contains the test cases for the search module."""

    def test_search(self, _, client: FlaskClient):
        """Test the search method."""

        url = "/search"

        # login
        AuthActions(client).login()

        # smoke test - don't follow redirects when testing redirect status
        response = client.get(url, follow_redirects=False)
        self.assertEqual(response.status_code, HttpRequestEnum.PERMANENT_REDIRECT.value)

        # logout
        AuthActions(client).logout()

    def test_search_result(self, _, client: FlaskClient):
        """Test the search result method."""

        url = "/search/results"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()
