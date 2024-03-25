# pylint: skip-file
"""Test data."""


class MockUser:
    """Mock register user data."""

    username = "test User"
    email = "test@gmail.com"
    password = "20240324!Group"
    confirm = "20240324!Group"
    avatar_url = None
    security_question = "What is your favorite color?"
    security_answer = "blue"

    def get_mock_user(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "confirm": self.confirm,
            "avatar_url": self.avatar_url,
            "security_question": self.security_question,
            "security_answer": self.security_answer,
        }
