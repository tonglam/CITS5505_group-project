""" User routes for the user blueprint."""

from flask import render_template
from flask_login import login_required

from app.extensions import db
from app.models.request import Request
from app.user import user_bp


@user_bp.route("/")
@login_required
def user():
    """Render the user page."""

    requests = db.session.query(Request).all()
    items = [{"id": request.id, "title": request.title} for request in requests]
    print("items: ", items)
    return render_template("user.html", items=items)
