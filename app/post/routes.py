"""Routes for post blueprint."""

from flask import render_template, request
from flask_login import current_user, login_required

from app.extensions import db
from app.models.community import Community
from app.models.reply import Reply
from app.models.request import Request
from app.models.tag import Tag
from app.models.user_like import UserLike
from app.models.user_record import UserRecord
from app.models.user_save import UserSave
from app.post import post_bp


@post_bp.route("/create/post", methods=["GET"])
@login_required
def create_post():
    """create post"""

    communities = Community.query.all()
    tags = Tag.query.all()

    return render_template(
        "create.html", mode="post", communities=communities, tags=tags
    )


@post_bp.route("/create/comment", methods=["GET"])
@login_required
def create_comment():
    """create comment"""

    post_id = request.args.get("post_id")

    target_type = request.args.get("target_type", "post")
    replies = Reply.query.filter_by(request_id=post_id).all()

    return render_template(
        "create.html",
        mode="comment",
        post_id=post_id,
        target_type=target_type,
        replies=replies,
    )


@post_bp.route("/edit/post", methods=["GET"])
@login_required
def edit_post():
    """edit post"""

    post_id = request.args.get("post_id")
    requests = Request.query.get_or_404(post_id)

    communities = Community.query.all()
    tags = Tag.query.all()

    return render_template(
        "create.html",
        mode="edit_post",
        communities=communities,
        tags=tags,
        requests=requests,
    )


@post_bp.route("/edit/comment", methods=["GET"])
@login_required
def edit_comment():
    """create comment"""

    post_id = request.args.get("post_id", type=int)
    reply_id = request.args.get("reply_id", type=int)
    target_type = request.args.get("target_type", "post")

    replies = Reply.query.get_or_404(reply_id)

    return render_template(
        "create.html",
        mode="edit_comment",
        post_id=post_id,
        target_type=target_type,
        reply_id=reply_id,
        replies=replies,
    )


@post_bp.route("/<int:post_id>", methods=["GET"])
@login_required
def post_detail(post_id: int):
    """show content by ID"""

    request_item = Request.query.get_or_404(post_id)
    replies = Reply.query.filter_by(request_id=post_id).all()

    user_id: str = current_user.id

    new_record = UserRecord(user_id=user_id, request_id=post_id)

    db.session.add(new_record)
    request_item.view_num += 1
    db.session.commit()

    # for likes and saves

    likes = (
        db.session.query(UserLike).filter_by(user_id=user_id, request_id=post_id).all()
    )
    user_likes = {like.reply_id for like in likes if like.reply_id is not None}
    post_likes = any(
        like.reply_id is None and like.request_id == post_id for like in likes
    )

    saves = (
        db.session.query(UserSave).filter_by(user_id=user_id, request_id=post_id).all()
    )
    user_saves = {save.reply_id for save in saves if save.reply_id is not None}
    post_saves = any(
        save.reply_id is None and save.request_id == post_id for save in saves
    )

    return render_template(
        "post.html",
        request=request_item,
        replies=replies,
        current_user=current_user,
        user_likes=user_likes,
        post_likes=post_likes,
        user_saves=user_saves,
        post_saves=post_saves,
    )
