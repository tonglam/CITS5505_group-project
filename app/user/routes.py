""" User routes for the user blueprint."""

from flask import current_app, render_template, request
from flask_login import login_required

from app.api.service import stats_service
from app.user import forms, user_bp
from app.user.service import history_data, like_data, post_data, save_data


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


@user_bp.route("/card")
def user_card():
    """Render the user card page."""

    stats_data = stats_service().json
    post_num = stats_data["data"]["stats"]["request_num"]

    return render_template("userProfile.html", post_num=post_num)
