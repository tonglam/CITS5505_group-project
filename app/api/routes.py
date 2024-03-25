"""Routes for api."""

from flask import request

from app.api import api_bp
from app.models.user import User

# Api for auth module.


@api_bp.route("/auth/email_exists")
def check_email_exists():
    """Check if the email exists."""
    email = request.args.get("email")
    print("check email:", email)
    user = User.query.filter_by(email=email).first()

    if user is not None:
        return {"message": "Email exists."}

    return {"message": "Email not exists."}


@api_bp.route("/auth/forgot_password_user")
def forgot_password_user():
    """Query the user for forgot password."""
    email = request.args.get("email")

    user = User.query.filter_by(email=email).first()

    if user is None:
        return {"message": "User not found"}

    return {"message": "User found", "user": user}


# Api for user module.


# Api for community module.


# Api for popular module.


# Api for post module.


# Api for search module.


# Api for notice module.
