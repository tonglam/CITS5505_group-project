"""Routes for popular blueprint."""

from flask import render_template
from flask_login import login_required

from ..popular import popular_bp


@login_required
@popular_bp.route("/")
def popular():
    """Render the popular page."""
    return render_template("popular.html")
