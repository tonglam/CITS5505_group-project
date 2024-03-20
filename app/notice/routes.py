"""This module contains the routes for the notice blueprint."""

from flask import render_template
from flask_login import login_required

from app.notice import notice_bp


@login_required
@notice_bp.route("/notice")
def notice():
    """Render the notice page."""
    return render_template("notice.html")
