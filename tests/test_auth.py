"""Tests for the auth module."""

import enum
import hashlib

from flask.testing import FlaskClient

from app.constants import GRAVATAR_URL
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

    def test_register(self, _, client: FlaskClient):
        """Test the registration process."""
        register_url = "/register"

        # smoke test
        self.assertStatus(client.get(register_url), 200)

        # test that successful registration redirects to the login page
        register_data = {
            "username": "test auth",
            "email": "test@gmail.com",
            "password": "Password@123",
            "confirm": "Password@123",
            "avatar_url": "https://api.dicebear.com/5.x/adventurer/svg?seed=5505",
            "security_question": "What is your favorite color?",
            "security_answer": "blue",
        }
        response = client.post(register_url, data=register_data)
        self.assertLocationHeader(response, "/login")

        # test that the user was inserted into the database
        user = User.query.filter_by(username=register_data["username"]).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, register_data["username"])
        self.assertEqual(user.email, register_data["email"])
        self.assertIn(
            user.avatar_url,
            [
                register_data["avatar_url"],
                f"{GRAVATAR_URL}{hashlib.sha256(user.email.lower().encode()).hexdigest()}",
            ],
        )
        self.assertEqual(user.security_question, register_data["security_question"])
        self.assertEqual(user.security_answer, register_data["security_answer"])

    def test_login(self, _, client: FlaskClient):
        """Test the login process."""

        login_url = "/login"

        # somke test
        self.assertStatus(client.get(login_url), 200)

        # test that successful login redirects to the home page
        login_data = {
            "email": seed_user_data[0]["email"],
            "password": seed_user_data[0]["password"],
        }
        response = client.post(login_url, data=login_data)
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
            response = auth.login(data["email"], data["password"])
            if data["type"] == InvalidLoginEnum.EMAIL_NOT_EXISTS:
                self.assertLocationHeader(response, "/register")
            else:
                self.assertLocationHeader(response, "/login")

    def test_logout(self, _, client: FlaskClient):
        """Test the logout process."""

        logout_url = "/logout"

        # test that successful logout redirects to the login page
        response = client.get(logout_url)
        self.assertLocationHeader(response, "/login?next=%2Flogout")

    def test_forgot_password(self, _, client: FlaskClient):
        """Test the forgot password process."""

        forgot_password_url = "/forgot_password"

        # smoke test
        self.assertStatus(client.get(forgot_password_url), 200)

        # test that successful forgot password redirects to the login page
        forgot_password_data = {
            "email": seed_user_data[0]["email"],
            "security_question": seed_user_data[0]["security_question"],
            "security_answer": seed_user_data[0]["security_answer"],
            "password": "Password@456",
            "confirm": "Password@456",
        }
        response = client.post(forgot_password_url, data=forgot_password_data)
        self.assertLocationHeader(response, "/login")

        # test that the user password was updated in the database
        user = User.query.filter_by(email=forgot_password_data["email"]).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.verify_password(forgot_password_data["password"]))

        # test login with the new password
        auth = AuthActions(client)
        response = auth.login(
            forgot_password_data["email"], forgot_password_data["password"]
        )
        self.assertLocationHeader(response, "/")

    def test_forgot_password_validate_input(self, _, client: FlaskClient):
        """Test the invalid forgot password process."""

        forgot_password_url = "/forgot_password"
        forgot_password_data = {
            "email": seed_user_data[0]["email"],
            "security_question": seed_user_data[0]["security_question"],
            "security_answer": seed_user_data[0]["security_answer"],
            "password": "Password@456",
            "confirm": "Password@456",
        }

        # test that the email is not valid
        forgot_password_data["email"] = seed_user_data[0]["email"] + "1"
        response = client.post(forgot_password_url, data=forgot_password_data)
        self.assertLocationHeader(response, "/forgot_password")

        # test that the security answer is not valid
        forgot_password_data["security_question"] = seed_user_data[0][
            "security_question"
        ]
        forgot_password_data["security_answer"] = (
            seed_user_data[0]["security_answer"] + "1"
        )
        response = client.post(forgot_password_url, data=forgot_password_data)
        self.assertLocationHeader(response, "/forgot_password")

        # test that the password is not valid
        forgot_password_data["security_answer"] = seed_user_data[0]["security_answer"]
        forgot_password_data["password"] = "123"
        response = client.post(forgot_password_url, data=forgot_password_data)
        self.assertLocationHeader(response, "/forgot_password")

        # test that the confirm password is not valid
        forgot_password_data["password"] = "Password@456"
        forgot_password_data["confirm"] = "Password@4567"
        response = client.post(forgot_password_url, data=forgot_password_data)
        self.assertLocationHeader(response, "/forgot_password")
