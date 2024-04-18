"""Tests for the API module."""

from flask import Flask
from flask.testing import FlaskClient

from app.constant import HttpRequstEnum
from app.models.user import User
from tests.config import TestBase
from tests.seeds.user_seeds import seed_user_data

_PREFIX = "/api/v1"


class TestApi(TestBase):
    """This class contains the test cases for the API module."""

    def test_get_users(self, app: Flask, client: FlaskClient):
        """Test the users GET API."""
        api_users_url = _PREFIX + "/users/"

        # check valid user
        user = None
        with app.app_context():
            user = User.query.filter_by(username=seed_user_data[0]["username"]).first()

        user_id = user.id

        response = client.get(api_users_url + user_id)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["user_id"], user_id)

        # check invalid user
        response = client.get(api_users_url + "invalid_user_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response_data["data"]["user_id"], "")

    def test_get_user_records(self, app: Flask, client: FlaskClient):
        """Test the user records GET API."""
        api_user_records_url = _PREFIX + "/users/records/"

        # # check valid user records
        # user = None
        # with app.app_context():
        #     user = User.query.filter_by(username=seed_user_data[0]["username"]).first()

        # user_id = user.id

        # response = client.get(api_user_records_url + user_id)
        # self.assertEqual(response.status_code, 200)

        # response_data = response.json
        # self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        # self.assertEqual(response_data["data"]["user_id"], user_id)

        # check invalid user
        response = client.get(api_user_records_url + seed_user_data[0]["username"])
        self.assertEqual(response.status_code, 200)
        print(response.json)

        # response_data = response.json
        # self.assertEqual(response_data["code"], HttpRequstEnum.BAD_REQUEST.value)
        # self.assertEqual(response_data["data"]["user_id"], "")
