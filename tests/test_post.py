"""Tests for the post module."""

from flask.testing import FlaskClient

from app.constants import HttpRequestEnum
from tests.config import AuthActions, TestBase


class TestPost(TestBase):
    """This class contains the test cases for the post module."""

    def test_get_post_detail(self, _, client: FlaskClient):
        """Test post detail page."""

        url = "/posts/1"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_create_post(self, _, client: FlaskClient):
        """Test create post page."""

        url = "/posts/create/post"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_create_comment(self, _, client: FlaskClient):
        """Test create comment page."""

        url = "/posts/create/comment"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_edit_post(self, _, client: FlaskClient):
        """Test edit post page."""

        url = "/posts/edit/post?post_id=1"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()
