""" User routes for the user blueprint."""

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.api.service import user_email_verify_service, user_verification_service
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


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Render the user profile page."""

    user_profile = db.session.query(User).filter_by(id=current_user.id).first()
    username = user_profile.username
    email = user_profile.email
    security_question = user_profile.security_question
    security_answer = user_profile.security_answer

    profile_form = forms.ProfileForm(request.form)

    if profile_form.validate_on_submit():

        if profile_form.username.data != username:
            verify_response = user_verification_service(
                profile_form.username.data
            ).get_json()
            verify_username = verify_response.get("data").get("result")

            if not verify_username:
                current_app.logger.error(
                    "Username exists, name: %s.", {profile_form.username.data}
                )
                flash("Username exists.", FlashAlertTypeEnum.DANGER.value)
                return redirect(url_for("user.profile"))

            user_profile.username = profile_form.username.data

        if profile_form.email.data != email:
            verify_email = user_email_verify_service(profile_form.email.data).get_json()
            verify_email = verify_email.get("data").get("result")

            if verify_email:
                current_app.logger.error(
                    "Username or E-mail exists, name: %s.", {profile_form.username.data}
                )
                flash("Username or E-mail exists.", FlashAlertTypeEnum.DANGER.value)
                return redirect(url_for("user.profile"))

            user_profile.email = profile_form.email.data

        if profile_form.security_question.data != security_question:
            user_profile.security_question = profile_form.security_question.data

        if profile_form.security_answer.data != security_answer:
            user_profile.security_answer = profile_form.security_answer.data

        # update user general profile
        db.session.commit()
        current_app.logger.info(
            "User profile updated, email: %s, id: %s.",
            {user_profile.email},
            {user_profile.id},
        )

        # send notification
        notice_event(
            user_id=user_profile.id, notice_type=NoticeTypeEnum.USER_UPDATED_PROFILE
        )

        current_app.logger.info("Profile updated for user, id: %s.", {user_profile.id})
        flash("Profile has been updated.", FlashAlertTypeEnum.SUCCESS.value)

    if profile_form.errors:
        for field, errors in profile_form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "Profile error in field %s: %s",
                    {getattr(profile_form, field).label.text},
                    {error},
                )
        return render_template("editprofile.html", form=profile_form)

    return render_template("editProfile.html", form=profile_form)


@user_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    """Render the user edit profile - password page."""

    password_form = forms.PasswordForm(request.form)
    user_profile = db.session.get(User, current_user.id)

    if password_form.validate_on_submit():
        if password_form.current_password.data and not user_profile.verify_password(
            password_form.current_password.data
        ):
            current_app.logger.error(
                "Invalid password with this email, email: %s.",
                {password_form.email.data},
            )

            flash(
                "Invalid password. Please try a different login method or attempt again.",
                FlashAlertTypeEnum.DANGER.value,
            )
            return redirect(url_for("user.profile"))

        user_profile.password = password_form.new_password.data

        # update user password
        db.session.commit()
        current_app.logger.info(
            "User password updated, email: %s, id: %s.",
            {user_profile.email},
            {user_profile.id},
        )

        # send notification
        notice_event(
            user_id=user_profile.id, notice_type=NoticeTypeEnum.USER_RESET_PASSWORD
        )

        current_app.logger.info("Password reset for user, id: %s.", {user_profile.id})
        flash("Password has been reset.", FlashAlertTypeEnum.SUCCESS.value)

        return redirect(url_for("user.profile"))

    if password_form.errors:
        for field, errors in password_form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "Password validate error in field %s: %s",
                    {getattr(password_form, field).label.text},
                    {error},
                )

        return redirect(url_for("user.profile"))

    return redirect(url_for("user.profile"))
