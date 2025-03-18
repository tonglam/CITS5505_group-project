"""Tests for the auth module."""

import enum

from flask.testing import FlaskClient

from app.constants import HttpRequestEnum
from app.models.user import User
from tests.config import AuthActions, TestBase
from tests.seeds.user_seeds import seed_user_data


class InvalidLoginEnum(enum.Enum):
    """Enum for invalid login type."""

    EMAIL_EMPTY = "Email empty"
    EMAIL_NOT_VALID = "Email not valid"
    EMAIL_NOT_EXISTS = "Email not exists"
    PASSWORD_EMPTY = "Password empty"
    PASSWORD_NOT_CORRECT = "Password not correct"


class TestAuth(TestBase):
    """This class contains the test cases for the authentication module."""

    def test_auth(self, _, client: FlaskClient):
        """Test the authentication page."""

        url = "/auth/auth"

        self.assertStatus(client.get(url), HttpRequestEnum.SUCCESS_OK.value)

    def test_register(self, _, client: FlaskClient):
        """Test the registration process."""

        url = "/auth/register"

        # test that successful registration redirects to the login page
        register_data = {
            "username": "test auth",
            "email": "test_auth@gmail.com",
            "password": "Password@123",
            "rpassword": "Password@123",
            "avatar": "https://api.dicebear.com/5.x/adventurer/svg?seed=5505",
            "squestion": "What is your favorite color?",
            "sanswer": "blue",
        }
        response = client.post(url, data=register_data)
        self.assertLocationHeader(response, "/auth/auth")

        # test that the user was inserted into the database
        user = User.query.filter_by(username=register_data["username"]).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, register_data["username"])
        self.assertEqual(user.email, register_data["email"])
        self.assertEqual(user.security_question, register_data["squestion"])
        self.assertEqual(user.security_answer, register_data["sanswer"])

    def test_login(self, _, client: FlaskClient):
        """Test the login process."""

        url = "/auth/login"

        # test that successful login redirects to the home page
        login_data = {
            "email": seed_user_data[0]["email"],
            "password": seed_user_data[0]["password"],
        }
        response = client.post(url, data=login_data)
        self.assertLocationHeader(response, "/")

    def test_login_validate_input(self, _, client: FlaskClient):
        """Test the invalid login process."""

        auth = AuthActions(client)
        auth_data = [
            {
                "email": "",
                "password": seed_user_data[0]["password"],
                "type": InvalidLoginEnum.EMAIL_EMPTY,
            },
            {
                "email": seed_user_data[0]["email"] + "1",
                "password": seed_user_data[0]["password"],
                "type": InvalidLoginEnum.EMAIL_NOT_VALID,
            },
            {
                "email": "1" + seed_user_data[0]["email"],
                "password": seed_user_data[0]["password"],
                "type": InvalidLoginEnum.EMAIL_NOT_EXISTS,
            },
            {
                "email": seed_user_data[0]["email"],
                "password": "",
                "type": InvalidLoginEnum.PASSWORD_EMPTY,
            },
            {
                "email": seed_user_data[0]["email"],
                "password": seed_user_data[0]["password"] + "1",
                "type": InvalidLoginEnum.PASSWORD_NOT_CORRECT,
            },
        ]

        for data in auth_data:
            response = auth.login(
                data["email"], data["password"], follow_redirects=False
            )

            if (
                data["type"] == InvalidLoginEnum.EMAIL_NOT_EXISTS
                or data["type"] == InvalidLoginEnum.PASSWORD_NOT_CORRECT
            ):
                self.assertStatus(response, HttpRequestEnum.FOUND.value)

    def test_logout(self, _, client: FlaskClient):
        """Test the logout process."""

        url = "/auth/logout"

        # test that successful logout redirects to the auth page
        response = client.get(url)
        self.assertLocationHeader(response, "/auth/auth?next=%2Fauth%2Flogout")

    def test_forgot_password(self, _, client: FlaskClient):
        """Test the forgot password process."""

        url = "/auth/forgot_password"

        # smoke test
        self.assertStatus(client.get(url), HttpRequestEnum.SUCCESS_OK.value)

        # test that successful forgot password redirects to the login page
        forgot_password_data = {
            "email": seed_user_data[0]["email"],
            "squestion": seed_user_data[0]["security_question"],
            "sanswer": seed_user_data[0]["security_answer"],
            "password": "Password@456",
            "rpassword": "Password@456",
        }
        response = client.post(url, data=forgot_password_data)
        self.assertLocationHeader(response, "/auth/auth")

        # test that the user password was updated in the database
        user = User.query.filter_by(email=forgot_password_data["email"]).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.verify_password(forgot_password_data["password"]))

        # test login with the new password
        auth = AuthActions(client)
        response = auth.login(
            forgot_password_data["email"],
            forgot_password_data["password"],
            follow_redirects=True,
        )
        self.assertStatus(response, HttpRequestEnum.SUCCESS_OK.value)

    def test_forgot_password_validate_input(self, _, client: FlaskClient):
        """Test the invalid forgot password process."""

        url = "/auth/forgot_password"
        forgot_password_data = {
            "email": seed_user_data[0]["email"],
            "squestion": seed_user_data[0]["security_question"],
            "sanswer": seed_user_data[0]["security_answer"],
            "password": "Password@456",
            "rpassword": "Password@456",
        }

        # test that the email is not valid
        forgot_password_data["email"] = seed_user_data[0]["email"] + "1"
        response = client.post(url, data=forgot_password_data)
        self.assertLocationHeader(response, "/auth/forgot_password")

        # test that the security answer is not valid
        forgot_password_data["squestion"] = seed_user_data[0]["security_question"]
        forgot_password_data["sanswer"] = seed_user_data[0]["security_answer"] + "1"
        response = client.post(url, data=forgot_password_data)
        self.assertLocationHeader(response, "/auth/forgot_password")

        # test that the password is not valid
        forgot_password_data["sanswer"] = seed_user_data[0]["security_answer"]
        forgot_password_data["password"] = "123"
        response = client.post(url, data=forgot_password_data)
        self.assertLocationHeader(response, "/auth/forgot_password")

        # test that the confirm password is not valid
        forgot_password_data["password"] = "Password@456"
        forgot_password_data["rpassword"] = "Password@4567"
        response = client.post(url, data=forgot_password_data)
        self.assertLocationHeader(response, "/auth/forgot_password")
