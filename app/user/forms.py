"""WTF form for user module."""

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class ProfileForm(FlaskForm):
    """WTF form for user profile."""

    username = StringField(
        name="name", validators=[DataRequired(), Length(min=2, max=50)]
    )

    email = EmailField(
        name="email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    security_question = StringField(name="squestion", validators=[DataRequired()])
    security_answer = StringField(name="sanswer", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    """WTF form for user password."""

    current_password = PasswordField(
        name="current_password", validators=[DataRequired(), Length(min=8, max=25)]
    )

    new_password = PasswordField(
        name="new_password",
        validators=[
            DataRequired(),
            Length(min=8, max=25),
            Regexp(
                r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]).{8,}$",
                message="Password must contain at least one uppercase letter, \
                    one lowercase letter, one digit, and one special character.",
            ),
        ],
    )

    rpassword = PasswordField(
        name="repeat_password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    submit = SubmitField("Submit")
