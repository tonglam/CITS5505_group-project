"""Tests for the API module."""

from flask import Flask
from flask.testing import FlaskClient

from app.constants import HttpRequstEnum
from app.models.category import Category
from app.models.tag import Tag
from app.models.user import User, UserStatusEnum
from app.models.user_preference import UserPreference
from app.models.user_record import UserRecord
from tests.config import AuthActions, TestBase

_PREFIX = "/api/v1"


class TestApi(TestBase):
    """This class contains the test cases for the API module."""

    def test_get_users(self, app: Flask, client: FlaskClient):
        """Test the users GET API."""

        url = _PREFIX + "/users/"

        # login
        AuthActions(client).login()

        # check valid data
        user = None
        with app.app_context():
            user = User.query.first()

        user_id = user.id

        response = client.get(url + user_id)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["user"]["id"], user_id)

        # check invalid data
        response = client.get(url + "invalid_user_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.NOT_FOUND.value)
        self.assertEqual(response_data["data"], None)

        # logout
        AuthActions(client).logout()

    def test_put_users(self, app: Flask, client: FlaskClient):
        """Test the users PUT API."""

        url = _PREFIX + "/users/"

        # login
        AuthActions(client).login()

        user = None
        with app.app_context():
            user = User.query.first()

        user_id = user.id

        update_data = {
            "username": "test_" + user.username,
            "email": "test_" + user.email,
            "avatar_url": "https://api.dicebear.com/5.x/adventurer/svg?seed=test",
            "use_google": True,
            "use_github": True,
            "security_question": "test_" + user.security_question,
            "security_answer": "test_" + user.security_answer,
            "status": UserStatusEnum.INACTIVE.value,
        }

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        # check the updated data
        update_username = response_data["data"]["user"]["username"]
        update_email = response_data["data"]["user"]["email"]
        update_avatar_url = response_data["data"]["user"]["avatar_url"]
        update_use_google = response_data["data"]["user"]["use_google"]
        update_use_github = response_data["data"]["user"]["use_github"]
        update_security_question = response_data["data"]["user"]["security_question"]
        update_security_answer = response_data["data"]["user"]["security_answer"]
        update_status = response_data["data"]["user"]["status"]

        self.assertEqual(update_username, "test_" + user.username)
        self.assertEqual(update_email, "test_" + user.email)
        self.assertEqual(
            update_avatar_url, "https://api.dicebear.com/5.x/adventurer/svg?seed=test"
        )
        self.assertEqual(update_use_google, True)
        self.assertEqual(update_use_github, True)
        self.assertEqual(update_security_question, "test_" + user.security_question)
        self.assertEqual(update_security_answer, "test_" + user.security_answer)
        self.assertEqual(update_status, UserStatusEnum.INACTIVE.value)

        # check db data
        with app.app_context():
            update_user = User.query.get(user_id)
            self.assertEqual(update_user.username, update_username)
            self.assertEqual(update_user.email, update_email)
            self.assertEqual(update_user.avatar_url, update_avatar_url)
            self.assertEqual(update_user.use_google, update_use_google)
            self.assertEqual(update_user.use_github, update_use_github)
            self.assertEqual(update_user.security_question, update_security_question)
            self.assertEqual(update_user.security_answer, update_security_answer)
            self.assertEqual(update_user.status, update_status)

        # logout
        AuthActions(client).logout()

    def test_invalid_put_users(self, app: Flask, client: FlaskClient):
        """Test the invalid users PUT API."""

        url = _PREFIX + "/users/"

        # login
        AuthActions(client).login()

        user = None
        with app.app_context():
            user = User.query.first()

        user_id = user.id

        # check empty data
        response = client.put(url + user_id, json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "request data is empty")

        # check if the username is a string
        update_data = {"username": 123}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[username] must be a string")

        # check if the username already exists
        another_user = None
        with app.app_context():
            another_user = User.query.filter(User.id != user_id).first()

        update_data = {"username": another_user.username}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[username] already exists")

        # check if the email is a string
        update_data = {"email": 123}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[email] must be a string")

        # check if the email is not a valid email
        update_data = {"email": user.email + ".invalid"}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[email] is invalid")

        # check if the avatar_url is a string
        update_data = {"avatar_url": 123}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[avatar_url] must be a string")

        # check if the use_google is a boolean
        update_data = {"use_google": 123}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[use_google] must be a boolean")

        # check if the use_github is a boolean
        update_data = {"use_github": 123}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[use_github] must be a boolean")

        # check if the security_question is a string
        update_data = {"security_question": 123}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(
            response.json["message"], "[security_question] must be a string"
        )

        # check if the security_answer is a string
        update_data = {"security_answer": 123}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[security_answer] must be a string")

        # check if the status is a string
        update_data = {"status": 123}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)

        # check if the status is invalid
        update_data = {"status": "invalid_status"}

        response = client.put(url + user_id, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[status] is invalid")

        # logout
        AuthActions(client).logout()

    def test_get_user_records(self, app: Flask, client: FlaskClient):
        """Test the user records GET API."""

        url = _PREFIX + "/users/records/"

        # login
        AuthActions(client).login()

        # check valid data
        user_record = None
        with app.app_context():
            user_record = UserRecord.query.first()

        user_id = user_record.user_id

        response = client.get(url + user_id)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        for record in response_data["data"]["records"]:
            self.assertEqual(record["user_id"], user_id)

        # check invalid data
        response = client.get(url + "invalid_user_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["records"], [])

        # logout
        AuthActions(client).logout()

    def test_delete_user_record(self, app: Flask, client: FlaskClient):
        """Test the user records DELETE API."""

        url = _PREFIX + "/users/records/"

        # login
        AuthActions(client).login()

        # check valid data
        record = None
        with app.app_context():
            record = UserRecord.query.first()

        record_id = record.id

        response = client.delete(url + str(record_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.NO_CONTENT.value)

        # check db
        with app.app_context():
            record = UserRecord.query.get(record_id)
            self.assertEqual(record, None)

        # check invalid data
        response = client.delete(url + "9999999999999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.NOT_FOUND.value)

        # logout
        AuthActions(client).logout()

    def test_get_user_preferences(self, app: Flask, client: FlaskClient):
        """Test the user preferences GET API."""

        url = _PREFIX + "/users/preferences/"

        # login
        AuthActions(client).login()

        # check valid data
        user_preference = None
        with app.app_context():
            user_preference = UserPreference.query.first()

        user_id = user_preference.user_id

        response = client.get(url + user_id)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        for record in response_data["data"]["preferences"]:
            self.assertEqual(record["user_id"], user_id)

        # check invalid data
        response = client.get(url + "invalid_user_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["preferences"], [])

        # logout
        AuthActions(client).logout()

    def test_put_user_preference(self, app: Flask, client: FlaskClient):
        """Test the user preferences PUT API."""

        url = _PREFIX + "/users/preferences/"

        # login
        AuthActions(client).login()

        user_preference = None
        with app.app_context():
            user_preference = UserPreference.query.first()

        preference_id = user_preference.id

        update_data = {
            "communities": "[test_community]",
            "interests": "[test_interest]",
        }

        response = client.put(url + str(preference_id), json=update_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        # check the updated data
        update_communities = response_data["data"]["preference"]["communities"]
        update_interests = response_data["data"]["preference"]["interests"]

        self.assertEqual(update_communities, "[test_community]")
        self.assertEqual(update_interests, "[test_interest]")

        # check db data
        with app.app_context():
            update_user = UserPreference.query.get(preference_id)
            self.assertEqual(update_user.communities, update_communities)
            self.assertEqual(update_user.interests, update_interests)

        # check empty data
        update_data = {}

        response = client.put(url + str(preference_id), json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "request data is empty")

        # check if the communities is a string
        update_data = {"communities": 123}

        response = client.put(url + str(preference_id), json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[communities] must be a string")

        # check if the interests is a string
        update_data = {"interests": 123}

        response = client.put(url + str(preference_id), json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["code"], HttpRequstEnum.BAD_REQUEST.value)
        self.assertEqual(response.json["message"], "[interests] must be a string")

        # logout
        AuthActions(client).logout()

    def test_get_categories(self, _, client: FlaskClient):
        """Test the categories GET API."""

        url = _PREFIX + "/categories"

        # login
        AuthActions(client).login()

        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_category(self, app: Flask, client: FlaskClient):
        """Test the category GET API."""

        url = _PREFIX + "/categories/"

        # login
        AuthActions(client).login()

        # check valid data
        category = None
        with app.app_context():
            category = Category.query.first()

        category_id = category.id

        response = client.get(url + str(category_id))
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["category"]["id"], category_id)

        # check invalid data
        response = client.get(url + "invalid_category_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.NOT_FOUND.value)
        self.assertEqual(response_data["data"], None)

        # logout
        AuthActions(client).logout()

    def test_get_tags(self, _, client: FlaskClient):
        """Test the tags GET API."""

        url = _PREFIX + "/tags"

        # login
        AuthActions(client).login()

        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)

        # logout
        AuthActions(client).logout()

    def test_get_tag(self, app: Flask, client: FlaskClient):
        """Test the tag GET API."""

        url = _PREFIX + "/tags/"

        # login
        AuthActions(client).login()

        # check valid data
        tag = None
        with app.app_context():
            tag = Tag.query.first()

        tag_id = tag.id

        response = client.get(url + str(tag_id))
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.SUCCESS_OK.value)
        self.assertEqual(response_data["data"]["tag"]["id"], tag_id)

        # check invalid data
        response = client.get(url + "invalid_tag_id")
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(response_data["code"], HttpRequstEnum.NOT_FOUND.value)
        self.assertEqual(response_data["data"], None)

        # logout
        AuthActions(client).logout()
