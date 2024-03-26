"""Test cases."""

import unittest

import flask_unittest
from flask.testing import FlaskClient

from app import create_app
from app.extensions import db
from app.models.user import User
from test_data import MockUser

mock_user_data = MockUser().get_mock_user()


class TestBase(flask_unittest.ClientTestCase):
    """This class contains the test cases for the base module."""

    test_user = None

    app = create_app()

    def create_mock_user(self, mock_user) -> User:
        """Create a mock user."""

        # check if the user already exists
        user = db.session.query(User).filter_by(email=mock_user["email"]).first()
        if user:
            return user

        # create the mock user
        user = User(
            username=mock_user["username"],
            email=mock_user["email"],
            avatar_url=mock_user["avatar_url"],
            use_google=False,
            use_github=False,
            security_question=mock_user["security_question"],
            security_answer=mock_user["security_answer"],
        )
        user.password = mock_user["password"]
        db.session.add(user)
        db.session.commit()

        return user

    def setUp(self, client: FlaskClient) -> None:
        """Set up the test case."""
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.test_user = self.create_mock_user(mock_user_data)
        client.post(
            "/login",
            data={
                "email": self.test_user.email,
                "password": mock_user_data["password"],
            },
        )

    def tearDown(self, client: FlaskClient) -> None:
        """Tear down the test case."""
        db.session.remove()
        self.appctx.pop()
        client.get("/logout")


class TestAuth(TestBase):
    """This class contains the test cases for the authentication module."""

    def test_register(self, client):
        """Test the registration of a new client."""

        # test the registration page, smoke test
        print("test register page")
        self.assertEqual(
            client.get("/register").status_code, 200, msg="Register page did not load"
        )

    def test_login(self, client):
        """Test the login of a user."""

        # test the login page, smoke test
        print("test login page")
        self.assertEqual(
            client.get("/login").status_code, 200, msg="Login page did not load"
        )

    def test_logout(self, client):
        """Test the logout of a user."""

        # test the logout of a user
        print("test logout test user")
        response = client.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_forgot_password(self, client):
        """Test the forgot password of a user."""

        # test the forgot password page, smoke test
        print("test forgot password page")
        self.assertEqual(
            client.get("/forgot_password").status_code,
            200,
            msg="Forgot password page did not load",
        )


class TestApi(TestBase):
    """This class contains the test cases for the API module."""

    def test_email_exists(self, client):
        """Test the get user API."""

        # test the email exists API
        print("test email exists")
        response = client.get(f"/api/v1/auth/email_exists?email={self.test_user.email}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Email exists.")

    def test_forgot_password_user(self, client):
        """Test the get user API."""

        # test the forgot password user API
        print("test forgot password user")
        response = client.get(
            f"/api/v1/auth/forgot_password_user?email={self.test_user.email}"
        )
        self.assertEqual(response.status_code, 200)
        print(response.json)
        self.assertEqual(response.json["message"], "User found")
        self.assertEqual(response.json["user"]["email"], self.test_user.email)


if __name__ == "__main__":
    unittest.main(verbosity=2)
    # unittest.main(verbosity=2, defaultTest="TestAuth")
    # unittest.main(verbosity=2, defaultTest='TestAuth.test_register')
