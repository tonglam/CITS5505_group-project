"""This module contains the routes for the community blueprint."""

from flask import render_template
from flask_login import login_required

from app.community import community_bp

@community_bp.route("/")
# @login_required
def community():
    """Render the community page."""
    list = [
            {"title": "Tech Community Component"}, 
            {"title": " Art Community Component"},
            {"title": " Travel Community Component"},
            {"title": " Astronomy Community Component"},
            {"title": " Medical Community Component"},
            {"title": " Economic Community Component"},
        ]
    return render_template("community.html",list=list)

@community_bp.route("/createCard")
# @login_required
def create():
    """Render the create page."""
    return render_template("createCard.html")



