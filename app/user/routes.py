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

    name_list = [
        post_result.get("name"),
        like_result.get("name"),
        history_result.get("name"),
        save_result.get("name"),
    ]
    data_list = [
        post_result.get("data"),
        like_result.get("data"),
        history_result.get("data"),
        save_result.get("data"),
    ]

    user_data = dict(zip(name_list, data_list))
    pagination = post_result.get("pagination")

    return render_template(
        "user.html",
        render_id="users-Posts",
        render_url="/users/lists?name=Posts",
        user_data=user_data,
        pagination=pagination,
    )


@user_bp.route("/lists", methods=["GET"])
@login_required
def user_lists():
    """Get the user's lists."""

    # name, required
    name = request.args.get("name", type=str)
    if name is None:
        return "Name is required", 400

    # pagination
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # retrieve data
    data_result = {}
    if name == "Posts":
        data_result = post_data(page, 5)
    elif name == "Likes":
        data_result = like_data(page, 5)
    elif name == "History":
        data_result = history_data(page, 5)
    elif name == "Wish":
        data_result = save_data(page, 5)

    pagination = data_result.get("pagination")

    return render_template(
        "userList.html",
        item=data_result.get("data"),
        pagination=pagination,
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
