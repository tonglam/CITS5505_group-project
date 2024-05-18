"""This module contains the routes for the search blueprint."""

from flask import render_template, request
from flask_login import login_required

from app.search import search_bp
from app.search.service import search_service


@search_bp.route("/", methods=["GET"])
@login_required
def search():
    """Render the search page."""
    return render_template("search.html")


@search_bp.route("/results", methods=["GET"])
@login_required
def search_result():
    """Render the search result page."""

    keyword = request.args.get("keyword")
    if not keyword:
        return render_template("searchResult.html", total_results="no")

    result = search_service(keyword)

    community_results = result.get("community")
    request_results = result.get("request")
    reply_results = result.get("reply")
    total_results = len(community_results) + len(request_results) + len(reply_results)

    return render_template(
        "searchResult.html",
        total_results=total_results,
        community_results=community_results,
        request_results=request_results,
        reply_results=reply_results,
    )
