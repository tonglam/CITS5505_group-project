"""This module contains the routes for the notice blueprint."""

from flask import render_template
from flask_login import login_required

from app.notice import notice_bp


@notice_bp.route("/notice")
@login_required
def notice():
    """Render the notice page."""

    return render_template("notice.html")
