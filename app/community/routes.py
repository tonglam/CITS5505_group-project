"""This module contains the routes for the community blueprint."""

from flask import render_template
from flask_login import login_required

from app.community import community_bp


@login_required
@community_bp.route("/")
def community():
    """Render the community page."""
    return render_template("community.html")
