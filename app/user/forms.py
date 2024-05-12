"""WTF form for user module."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class ProfileForm(FlaskForm):
    """WTF form for user profile."""

    avatar = FileField(
        "avatar", validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")]
    )
    username = StringField(
        "username", validators=[DataRequired(), Length(min=2, max=50)]
    )
    email = EmailField(
        "email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    security_question = StringField("security_question", validators=[DataRequired()])
    security_answer = StringField("security_answer", validators=[DataRequired()])


class PasswordForm(FlaskForm):
    """WTF form for user password."""

    current_password = PasswordField(name="current_password")
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
            EqualTo("new_password", message="Passwords must match."),
        ],
    )
