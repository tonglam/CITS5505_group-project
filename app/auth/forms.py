"""This module contains the forms."""

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Optional,
                                Regexp)


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=50)]
    )
    email = EmailField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=25),
            Regexp(
                r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]).{8,}$",
                message="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
            ),
        ],
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    avatar_url = StringField("Avatar", validators=[Optional()])
    security_question = StringField("Security Question", validators=[DataRequired()])
    security_answer = StringField("Security Answer", validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Login form."""

    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )


class ForgotPasswordForm(FlaskForm):
    """Forgot password form."""

    email = EmailField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    security_question = StringField("Security Question", validators=[DataRequired()])
    security_answer = StringField("Security Answer", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=25),
            Regexp(
                r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]).{8,}$",
                message="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
            ),
        ],
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
