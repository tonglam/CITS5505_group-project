"""This module contains the routes for the search blueprint."""

from flask import render_template
from flask_login import login_required

from app.search import search_bp


@search_bp.route("/search")
@login_required
def search():
    """Render the search page."""
    return render_template("search.html")
