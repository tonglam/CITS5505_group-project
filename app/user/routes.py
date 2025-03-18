""" User routes for the user blueprint."""

from flask import (abort, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required

from app.api.service import (user_email_verify_service,
                             user_verification_service)
from app.constants import FlashAlertTypeEnum, HttpRequestEnum
from app.extensions import db
from app.models.user import User
from app.notice.events import NoticeTypeEnum, notice_event
from app.user import forms, user_bp
from app.user.service import (display_community_data, get_upload_avatar_url,
                              history_data, like_data, post_data, save_data,
                              stat_data)


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

    # display user community
    display_user_communities = display_community_data()

    return render_template(
        "user.html",
        render_id="users-Posts",
        render_url="/users/lists?name=Posts",
        user_stat=user_stat,
        user_data=user_data,
        display_user_communities=display_user_communities,
        pagination=pagination,
    )


@user_bp.route("/lists", methods=["GET"])
@login_required
def user_lists():
    """Get the user's lists."""

    # name, required
    name = request.args.get("name", type=str)
    if name is None:
        abort(HttpRequestEnum.BAD_REQUEST.value)

    # pagination
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

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


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
def user_profile():
    """Get the user's profile account page."""

    user_id = current_user.id
    profile_form = forms.ProfileForm()

    if profile_form.validate_on_submit():
        user_entity = db.session.query(User).filter_by(id=user_id).first()

        update = False

        avatar_file = profile_form.avatar.data
        username = user_entity.username
        email = user_entity.email
        security_question = user_entity.security_question
        security_answer = user_entity.security_answer

        if profile_form.avatar.data:
            upload_avatar_url = get_upload_avatar_url(avatar_file)
            current_user.avatar_url = upload_avatar_url
            user_entity.avatar_url = upload_avatar_url
            update = True

        if profile_form.username.data != username:
            # verify username
            verify_username = (
                user_verification_service(profile_form.username.data)
                .get_json()
                .get("data")
                .get("result")
            )

            if not verify_username:
                current_app.logger.error("Username: %s exists.", {username})
                flash("Username exists.", FlashAlertTypeEnum.DANGER.value)
                return redirect(url_for("user.profile"))

            user_entity.username = profile_form.username.data
            update = True

        if profile_form.email.data != email:
            # verify email
            verify_email = (
                user_email_verify_service(profile_form.email.data)
                .get_json()
                .get("data")
                .get("result")
            )

            if verify_email:
                current_app.logger.error("Email: %s exists", {username})
                flash("E-mail exists.", FlashAlertTypeEnum.DANGER.value)
                return redirect(url_for("user.profile"))

            user_entity.email = profile_form.email.data
            update = True

        if profile_form.security_question.data != security_question:
            user_entity.security_question = profile_form.security_question.data
            update = True

        if profile_form.security_answer.data != security_answer:
            user_entity.security_answer = profile_form.security_answer.data
            update = True

        if update:
            # update user general profile
            db.session.commit()
            current_app.logger.info("User: %s profile updated.", {username})

            # send notification
            notice_event(notice_type=NoticeTypeEnum.USER_UPDATED_PROFILE)

            current_app.logger.info("Profile updated for user: %s.", {username})
            flash("Profile has been updated.", FlashAlertTypeEnum.SUCCESS.value)

    if profile_form.errors:
        for field, errors in profile_form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "User %s edit profile error in field %s: %s",
                    {username},
                    {getattr(profile_form, field).label.text},
                    {error},
                )
                flash(
                    f"{getattr(profile_form, field).label.text}, {error}",
                    FlashAlertTypeEnum.DANGER.value,
                )
        return redirect(url_for("user.user_profile"))

    return render_template("userProfile.html", tab="profile", form=profile_form)


@user_bp.route("/password", methods=["GET", "POST"])
@login_required
def user_password():
    """Get the user's profile password page."""

    user_id = current_user.id
    password_form = forms.PasswordForm(request.form)

    if password_form.validate_on_submit():
        user_entity = db.session.query(User).filter_by(id=user_id).first()

        username = user_entity.username
        current_password = password_form.current_password.data
        new_password = password_form.new_password.data

        if not current_password:
            flash("Password not changed.", FlashAlertTypeEnum.DANGER.value)
            return render_template(
                "userPassword.html", tab="password", form=password_form
            )

        if not user_entity.verify_password(current_password):
            current_app.logger.error("Invalid password for user: %s.", {username})

            flash(
                "Invalid password. Please try again.",
                FlashAlertTypeEnum.DANGER.value,
            )

        user_entity.password = new_password

        # update user password
        db.session.commit()
        current_app.logger.info("User: %s password updated.", {username})

        # send notification
        notice_event(notice_type=NoticeTypeEnum.USER_RESET_PASSWORD)

        current_app.logger.info("Password reset for user: %s.", {username})
        flash("Password has been reset.", FlashAlertTypeEnum.SUCCESS.value)

        return redirect(url_for("auth.auth"))

    if password_form.errors:
        for field, errors in password_form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "User: %s edit profile error in field %s: %s",
                    {username},
                    {getattr(password_form, field).label.text},
                    {error},
                )
                flash(
                    f"{getattr(password_form, field).label.text}, {error}",
                    FlashAlertTypeEnum.DANGER.value,
                )
        return redirect(url_for("user.user_password"))

    return render_template("userPassword.html", tab="password", form=password_form)


@user_bp.route("/info", methods=["GET"])
@login_required
def user_info():
    """Get the user's profile info."""

    return render_template("userInfo.html", tab="info")


@user_bp.route("/notification", methods=["GET"])
@login_required
def user_notification():
    """Get the user's profile notification."""

    return render_template("userNotification.html", tab="notification")
