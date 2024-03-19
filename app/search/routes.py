"""This module contains the routes for the search blueprint."""

from flask import render_template
from flask_login import login_required

from ..search import search_bp


@login_required
@search_bp.route("/search")
def search():
    """Render the search page."""
    return render_template("search.html")
