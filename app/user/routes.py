""" User routes for the user blueprint."""

from flask import current_app, render_template, request
from flask_login import login_required

from app.user import forms, user_bp
from app.user.service import history_data, like_data, post_data, save_data


@user_bp.route("/")
@login_required
def user():
    """Render the user page."""

    post_result = post_data(1, 5)
    like_result = like_data(1, 5)
    history_result = history_data(1, 5)
    save_result = save_data(1, 5)

    return render_template(
        "user.html",
        render_id="users-posts",
        render_url="/users/posts",
        post=post_result,
        like=like_result,
        history=history_result,
        save=save_result,
    )


@user_bp.route("/posts", methods=["GET"])
@login_required
def user_posts():
    """Get the user's posts."""

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    post_result = post_data(page, 5)
    print("post_result:", post_result)

    return render_template(
        "userPostList.html",
        post=post_result,
    )


@user_bp.route("/likes", methods=["GET"])
@login_required
def user_likes():
    """Get the user's likes."""

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    like_result = like_data(page, 5)

    return render_template(
        "userLikeList.html",
        like=like_result,
    )


@user_bp.route("/histories", methods=["GET"])
@login_required
def user_histories():
    """Get the user's histories."""

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    history_result = history_data(page, 5)

    return render_template(
        "userHistoryList.html",
        history=history_result,
    )


@user_bp.route("/wishes", methods=["GET"])
@login_required
def user_wishes():
    """Get the user's wishes."""

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    save_result = save_data(page, 5)

    return render_template(
        "userWishList.html",
        save=save_result,
    )


@user_bp.route("/profile", methods=["GET", "PUT"])
@login_required
def profile():
    """Render the user profile page."""

    form = forms.ProfileForm(request.form)

    if form.validate_on_submit():
        # update user profile
        pass

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "Forgot password error in field %s: %s",
                    {getattr(form, field).label.text},
                    {error},
                )
        return render_template("userProfile.html", form=form)

    return render_template("userProfile.html", form=form)
