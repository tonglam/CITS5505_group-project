"""Tests for the API module."""

from flask import Flask
from flask.testing import FlaskClient

from app.constant import HttpRequstEnum
from app.models.category import Category
from app.models.tag import Tag
from app.models.user import User
from app.models.user_preference import UserPreference
from app.models.user_record import UserRecord
from tests.config import TestBase

_PREFIX = "/api/v1"


class TestApi(TestBase):
    """This class contains the test cases for the API module."""

    def test_get_users(self, app: Flask, client: FlaskClient):
        """Test the users GET API."""

        users_api_url = _PREFIX + "/users/"

        # check valid data
        user = None
        with app.app_context():
            user = User.query.first()

        user_id = user.id

        response = client.get(users_api_url + user_id)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["user_id"], user_id)

        # check invalid data
        response = client.get(users_api_url + "invalid_user_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response_data["data"]["user_id"], "")

    def test_get_user_records(self, app: Flask, client: FlaskClient):
        """Test the user records GET API."""

        user_records_api_url = _PREFIX + "/users/records/"

        # check valid data
        user_record = None
        with app.app_context():
            user_record = UserRecord.query.first()

        user_id = user_record.user_id

        response = client.get(user_records_api_url + user_id)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        for record in response_data["data"]["records"]:
            self.assertEqual(record["user_id"], user_id)

        # check invalid data
        response = client.get(user_records_api_url + "invalid_user_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["records"], [])

    def test_get_user_preferences(self, app: Flask, client: FlaskClient):
        """Test the user preferences GET API."""

        user_preferences_api_url = _PREFIX + "/users/preferences/"

        # check valid data
        user_preference = None
        with app.app_context():
            user_preference = UserPreference.query.first()

        user_id = user_preference.user_id

        response = client.get(user_preferences_api_url + user_id)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        for record in response_data["data"]["preferences"]:
            self.assertEqual(record["user_id"], user_id)

        # check invalid data
        response = client.get(user_preferences_api_url + "invalid_user_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["preferences"], [])

    def test_get_categories(self, _, client: FlaskClient):
        """Test the categories GET API."""

        categories_api_url = _PREFIX + "/categories"

        response = client.get(categories_api_url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

    def test_get_category(self, app: Flask, client: FlaskClient):
        """Test the category GET API."""

        category_api_url = _PREFIX + "/categories/"

        # check valid data
        category = None
        with app.app_context():
            category = Category.query.first()

        category_id = category.id

        response = client.get(category_api_url + str(category_id))
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["category"]["id"], category_id)

        # check invalid data
        response = client.get(category_api_url + "invalid_category_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response_data["data"]["category"], "")

    def test_get_tags(self, _, client: FlaskClient):
        """Test the tags GET API."""

        tags_api_url = _PREFIX + "/tags"

        response = client.get(tags_api_url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

    def test_get_tag(self, app: Flask, client: FlaskClient):
        """Test the tag GET API."""

        tag_api_url = _PREFIX + "/tags/"

        # check valid data
        tag = None
        with app.app_context():
            tag = Tag.query.first()

        tag_id = tag.id

        response = client.get(tag_api_url + str(tag_id))
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["tag"]["id"], tag_id)

        # check invalid data
        response = client.get(tag_api_url + "invalid_tag_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response_data["data"]["tag"], "")
