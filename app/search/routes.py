"""This module contains the routes for the search blueprint."""

from flask import abort, render_template, request
from flask_login import login_required

from app.api.service import search_service
from app.constants import HttpRequstEnum
from app.search import search_bp


@search_bp.route("/")
@login_required
def search():
    """Render the search page."""
    return render_template("search.html")


@search_bp.route("/results")
def search_result():
    """Render the search result page."""

    keyword = request.args.get("keyword")
    if not keyword:
        return render_template("searchResult.html", total_results="no")

    result = search_service(keyword).json

    result_status = result.get("code")
    if result_status != HttpRequstEnum.SUCCESS_OK.value:
        abort(result_status)

    result_data = result.get("data")

    community_list = result_data.get("community")
    print("community: ", community_list[0])
    request_list = result_data.get("request")
    print("request: ", request_list[0])
    reply_list = result_data.get("reply")
    print("reply: ", reply_list[0])

    total_results = len(community_list) + len(request_list) + len(reply_list)

    return render_template(
        "searchResult.html",
        total_results=total_results,
        community_list=community_list,
        request_list=request_list,
        reply_list=reply_list,
    )
