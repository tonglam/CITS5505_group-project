"""Routes for post blueprint."""

from flask import render_template
from flask_login import login_required

from ..post import post_bp


@login_required
@post_bp.route("/create")
def create():
    """Render the create page."""
    return render_template("create.html")
