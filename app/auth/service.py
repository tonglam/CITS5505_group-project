"""This module contains the service layer for the authentication blueprint."""

from wtforms import Form, PasswordField, StringField, validators

from app.models.user import User


def register(user: User) -> None:
    """Register a new user."""
    print(user.username, user.password, user.email, user.phone, user.avatar)


def login(username: str, password: str) -> None:
    """Log in the user."""
    print(username, password)


class RegisterForm(Form):
    """Register form."""

    username = StringField("registerUsername", [validators.Length(min=4, max=25)])
    email = StringField("registerEmail", [validators.Length(min=6, max=35)])
    password = PasswordField(
        "registerPassword",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("registerRepeatPassword")
