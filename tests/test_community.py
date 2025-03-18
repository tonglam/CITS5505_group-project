"""Tests for the community module."""

from flask import Flask
from flask.testing import FlaskClient

from app.constants import HttpRequestEnum
from app.models.community import Community
from app.models.user import User
from tests.config import AuthActions, TestBase


class TestCommunity(TestBase):
    """This class contains the test cases for the community module."""

    def test_get_community(self, _, client: FlaskClient):
        """Test community page."""

        url = "/communities/"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_community_list(self, _, client: FlaskClient):
        """Test community page re-render."""

        url = "/communities/community_list"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_community(self, _, client: FlaskClient):
        """Test user community page."""

        url = "/communities/community_list/user"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_community_list(self, _, client: FlaskClient):
        """Test user community page re-render."""

        url = "/communities/community_list/user"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_community_management(self, _, client: FlaskClient):
        """Test community management page."""

        url = "/communities/management"

        # login
        AuthActions(client).login()

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        community = Community.query.first()
        url = f"/communities/management/{community.id}"

        # smoke test
        response = client.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_post_community_management(self, app: Flask, client: FlaskClient):
        """Test community management page post request."""

        community = None
        user = None
        with app.app_context():
            community = Community.query.first()
            user = User.query.filter_by(id=community.creator_id).first()

        url = "/communities/management"

        # login
        AuthActions(client).login(email=user.email, password="Password@123")

        # create community
        response = client.post(
            url,
            data={
                "name": "test",
                "category_select": 1,
                "description": "test",
                "avatar_url": "test",
                "creator_id": user.id,
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # check if community is created
        with app.app_context():
            community = Community.query.filter_by(name="test").first()
            self.assertIsNotNone(community)

        url = f"/communities/management/{community.id}"

        # update community
        response = client.post(
            url,
            data={
                "name": "test",
                "category_select": 2,
                "description": "test",
                "avatar_url": "test",
                "creator_id": user.id,
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, HttpRequestEnum.SUCCESS_OK.value)

        # check if community is updated
        with app.app_context():
            community = Community.query.filter_by(name="test").first()
            self.assertEqual(community.category_id, 2)

        # logout
        AuthActions(client).logout()
