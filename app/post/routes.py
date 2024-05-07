"""Routes for post blueprint."""

from flask import render_template

from app.models.reply import Reply
from app.models.request import Request
from app.post import post_bp


@post_bp.route('/create_post')
def create_post():
    """create post"""

    return render_template('create.html', mode='post')

@post_bp.route('/create_comment')
def create_comment():
    """create comment"""

    return render_template('create.html', mode='comment')

@post_bp.route("/<int:post_id>")
def post_detail(post_id):
    """show content by ID"""

    request_item = Request.query.get_or_404(post_id)
    replies = Reply.query.filter_by(request_id = post_id).all()

    return render_template("post.html", request=request_item, replies=replies)
