""" User routes for the user blueprint."""

from flask import render_template
from flask_login import login_required

from app.user import user_bp


@login_required
@user_bp.route("/")
def user():
    """Render the user page."""
    return render_template("user.html")
