"""Routes for popular blueprint."""

from flask import render_template
from flask_login import login_required

from app.popular.service import (top_community_service, top_replied_service,
                                 top_viewed_service)

from . import popular_bp


@popular_bp.route("/", methods=["GET"])
@login_required
def popular():
    """Render the popular page."""

    # top replied data
    top_replied = top_replied_service()

    # top viewed data
    top_viewed = top_viewed_service()

    # top community data
    top_community = top_community_service()

    return render_template(
        "popular.html",
        topReplies=top_replied,
        topViews=top_viewed,
        topCommunities=top_community,
    )
