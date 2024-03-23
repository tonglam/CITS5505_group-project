"""Routes for popular blueprint."""

from flask import render_template
from flask_login import login_required

from app.popular import popular_bp


@popular_bp.route("/")
@login_required
def popular():
    """Render the popular page."""
    return render_template("popular.html")
