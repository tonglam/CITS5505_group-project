"""This module contains the routes for the notice blueprint."""

from flask import render_template
from flask_login import login_required

from app.api.service import users_notices_service
from app.notice import notice_bp


@notice_bp.route("/")
@login_required
def notice():
    """Render the notice page."""

    notice = users_notices_service().get_json().get("data").get("user_notices")
    print("notice: ", notice)

    return render_template("notice.html")
