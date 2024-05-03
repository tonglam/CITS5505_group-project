""" User routes for the user blueprint."""

from flask import render_template
from flask_login import login_required

from app.api.routes import user_likes, user_posts, user_records, user_saves
from app.user import user_bp


@user_bp.route("/")
@login_required
def user():
    """Render the user page."""

    post_result = post_data()
    like_result = like_data()
    history_result = history_data()
    save_result = save_data()

    return render_template(
        "user.html",
        posts=post_result,
        likes=like_result,
        history=history_result,
        WishList=save_result,
    )


def post_data():
    """Get the user's posts."""

    posts = user_posts()
    posts_data = posts.get_json()
    user_post_data = posts_data["data"]["user_posts"]
    posts_title = [{"title": post["title"]} for post in user_post_data]
    post_page = posts_data["pagination"]
    post_result = {"data": posts_title, "page": post_page}

    return post_result


def like_data():
    """Get the user's likes."""
    likes = user_likes()
    likes_data = likes.get_json()
    user_likes_data = likes_data["data"]["user_likes"]
    likes_title = [{"title": like["request_title"]} for like in user_likes_data]
    like_page = likes_data["pagination"]
    like_result = {"data": likes_title, "page": like_page}

    return like_result


def history_data():
    """Get the user's history."""
    histories = user_records()
    histories_data = histories.get_json()
    user_histories_data = histories_data["data"]["user_records"]
    histories_title = [
        {"title": history["request_title"]} for history in user_histories_data
    ]

    history_page = histories_data["pagination"]
    history_result = {"data": histories_title, "page": history_page}

    return history_result


def save_data():
    """Get the user's wishlist."""
    saves = user_saves()
    saves_data = saves.get_json()
    user_saves_data = saves_data["data"]["user_saves"]
    saves_title = [{"title": save["request_title"]} for save in user_saves_data]
    save_page = saves_data["pagination"]
    save_result = {"data": saves_title, "page": save_page}

    return save_result
