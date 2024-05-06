""" User routes for the user blueprint."""

from flask import current_app, render_template, request
from flask_login import login_required

from app.user import forms, user_bp


@user_bp.route("/")
@login_required
def user():
    """Render the user page."""

    return render_template("user.html")


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
