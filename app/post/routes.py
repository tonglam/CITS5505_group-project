"""Routes for post blueprint."""

from flask import render_template
from flask_login import login_required
from app.models.request import Request
from app.models.reply import Reply


from app.post import post_bp


@post_bp.route("/create")
@login_required
def create():
    """Render the create page."""
    return render_template("create.html")

@post_bp.route("/<int:post_id>")
def post_detail(post_id):
    """show content by ID"""

    request_item = Request.query.get_or_404(post_id)
    replies = Reply.query.filter_by(request = post_id).all()
    return render_template("post.html", request=request_item, replies=replies)
