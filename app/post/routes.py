"""Routes for post blueprint."""

from flask import render_template
from flask_login import login_required

from app.post import post_bp


@post_bp.route("/create")
@login_required
def create():
    """Render the create page."""
    return render_template("create.html")
