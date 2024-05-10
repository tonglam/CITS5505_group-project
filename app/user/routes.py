""" User routes for the user blueprint."""

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.constants import FlashAlertTypeEnum
from app.extensions import db
from app.models.user import User
from app.notice.events import NoticeTypeEnum, notice_event
from app.user import forms, user_bp
from app.user.service import (
    community_data,
    history_data,
    like_data,
    post_data,
    save_data,
    stat_data,
)


@user_bp.route("/")
@login_required
def user():
    """Render the user page."""

    # user data
    post_result = post_data()
    like_result = like_data()
    history_result = history_data()
    save_result = save_data()

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

    # user stat
    user_stat = stat_data()

    # user community
    user_communities = community_data()

    return render_template(
        "user.html",
        render_id="users-Posts",
        render_url="/users/lists?name=Posts",
        user_stat=user_stat,
        user_data=user_data,
        user_communities=user_communities,
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
        data_result = post_data(page, per_page)
    elif name == "Likes":
        data_result = like_data(page, per_page)
    elif name == "History":
        data_result = history_data(page, per_page)
    elif name == "Collects":
        data_result = save_data(page, per_page)

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

    profile_form = forms.ProfileForm(request.form)

    if profile_form.validate_on_submit():
        user = User.query.filter_by(email=profile_form.email.data).first()
        if user is None:
            current_app.logger.error(
                "No user with that email exists, email: %s.", {profile_form.email.data}
            )
            flash("No user with that email exists.", FlashAlertTypeEnum.DANGER.value)

        if user.security_answer != profile_form.security_answer.data:
            current_app.logger.error(
                "Invalid security answer, email: %s, security answer: %s.",
                {profile_form.email.data},
                {profile_form.security_answer.data},
            )
            flash("Invalid security answer.", FlashAlertTypeEnum.DANGER.value)
            user.password = password_form.password.data

        # update user password
        db.session.commit()
        current_app.logger.info(
            "User profile updated, email: %s, id: %s.", {user.email}, {user.id}
        )

        # send notification
        notice_event(user_id=user.id, notice_type=NoticeTypeEnum.USER_RESET_PASSWORD)

        current_app.logger.info("Password reset for user, id: %s.", {user.id})
        flash("Password has been reset.", FlashAlertTypeEnum.SUCCESS.value)

    if profile_form.errors:
        for field, errors in profile_form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "Forgot password error in field %s: %s",
                    {getattr(profile_form, field).label.text},
                    {error},
                )

    return render_template("editProfile.html", form=profile_form)


@user_bp.route("/profile", methods=["GET", "PUT"])
@login_required
def change_password():
    """Render the user edit profile - password page."""

    password_form = forms.PasswordForm(request.form)

    if password_form.validate_on_submit():
        user = User.query.filter_by(email=password_form.email.data).first()
        if user is None:
            current_app.logger.error(
                "No user with that email exists, email: %s.", {password_form.email.data}
            )
            flash("No user with that email exists.", FlashAlertTypeEnum.DANGER.value)

        if user.security_answer != password_form.security_answer.data:
            current_app.logger.error(
                "Invalid security answer, email: %s, security answer: %s.",
                {password_form.email.data},
                {password_form.security_answer.data},
            )
            flash("Invalid security answer.", FlashAlertTypeEnum.DANGER.value)
            return redirect(url_for("auth.forgot_password"))

        user.password = password_form.password.data

        # update user password
        db.session.commit()
        current_app.logger.info(
            "User password updated, email: %s, id: %s.", {user.email}, {user.id}
        )

        # send notification
        notice_event(user_id=user.id, notice_type=NoticeTypeEnum.USER_RESET_PASSWORD)

        current_app.logger.info("Password reset for user, id: %s.", {user.id})
        flash("Password has been reset.", FlashAlertTypeEnum.SUCCESS.value)

    if password_form.errors:
        for field, errors in password_form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "Forgot password error in field %s: %s",
                    {getattr(password_form, field).label.text},
                    {error},
                )

    return render_template("editProfile.html", form=password_form)
