"""Routes for api."""

from app.api import api_bp
from app.models.user import User

# Api for auth module.


@api_bp.route("/check_email_exists/<email>")
def check_email_exists(email: str):
    """Check if the email exists."""
    print("check email:", email)
    user = User.query.filter_by(email=email).first()

    if user is not None:
        return {"message": "Email exists."}

    return {"message": "Email not exists."}


@api_bp.route("/query_forgot_password_user/<email>")
def query_forgot_password_user(email: str):
    """Query the user for forgot password."""
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
