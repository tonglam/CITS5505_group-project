"""Routes for authentication."""

import secrets
from urllib.parse import urlencode

import requests
from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_jwt_extended import create_access_token, set_access_cookies
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import auth_bp, forms
from app.constants import (
    AUTHORIZATION_CODE,
    AUTHORIZE_URL,
    CALLBACK_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    OAUTH2_PROVIDERS,
    OAUTH2_STATE,
    RESPONSE_TYPE,
    SCOPES,
    TOKEN_URL,
    FlashAlertTypeEnum,
    HttpRequstEnum,
    OAuthProviderEnum,
)
from app.extensions import db, login_manager
from app.models.user import User
from app.notice.events import NoticeTypeEnum, notice_event


@login_manager.user_loader
def user_loader(user_id: str):
    """Given *user_id*, return the associated User object."""

    return db.session.get(User, user_id)


@auth_bp.route("/auth", methods=["GET"])
def auth():
    """verification page."""

    form = forms.RegisterForm()
    return render_template("auth.html", form=form)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""

    if current_user.is_authenticated:
        current_app.logger.info(
            "User is already registered, id: %s.", {current_user.id}
        )
        flash("You are already registered.", FlashAlertTypeEnum.SUCCESS.value)
        return redirect(url_for("auth.auth"))

    form = forms.RegisterForm(request.form)

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if user.password_hash:
                # registered with email and password before
                current_app.logger.error(
                    "Email already registered, email: %s.", {form.email.data}
                )
                flash("Email already registered.", FlashAlertTypeEnum.DANGER.value)
                return redirect(url_for("auth.auth"))

            # only login with third party OAuth before
            user.username = form.username.data
            user.email = form.email.data
            user.avatar_url = (
                form.avatar_url.data if form.avatar_url.data else user.avatar_url
            )
            user.security_question = form.security_question.data
            user.security_answer = form.security_answer.data
            user.password = form.password.data

        else:

            # add a new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                avatar_url=form.avatar_url.data,
                use_google=False,
                use_github=False,
                security_question=form.security_question.data,
                security_answer=form.security_answer.data,
            )
            user.password = form.password.data
            db.session.add(user)

        db.session.commit()
        login_user(user, remember=True)
        current_app.logger.info(
            "User registered, register email: %s, id: %s.", {user.email}, {user.id}
        )
        flash("You registered and are now logged in.", FlashAlertTypeEnum.SUCCESS.value)
        return redirect(url_for("auth.auth"))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "Register error in field %s: %s",
                    {getattr(form, field).label.text},
                    {error},
                )
        return render_template("auth.html", form=form)

    abort(HttpRequstEnum.METHOD_NOT_ALLOWED.value)


@auth_bp.route("/login", methods=["POST"])
def login():
    """user login."""

    form = forms.LoginForm(request.form)
    if form.validate_on_submit():

        email = form.email.data

        user = User.query.filter_by(email=email).first()

        if user is None:
            current_app.logger.error("No user with that email exists: %s.", {email})
            flash(
                "No user with that email exists, please register first.",
                FlashAlertTypeEnum.DANGER.value,
            )
            return redirect(url_for("auth.auth"))

        if not user.password_hash:
            provide = "Google" if user.use_google else "GitHub"
            current_app.logger.error(
                "Please login with %s, email: %s.", {provide}, {email}
            )
            flash(f"Please login with {provide}.", FlashAlertTypeEnum.WARNING.value)
            return redirect(url_for("auth.auth"))

        if not user.verify_password(form.password.data):
            current_app.logger.error("Invalid email or password, email: %s.", {email})

            flash(
                "Invalid email or password. Please try a different login method or attempt again.",
                FlashAlertTypeEnum.DANGER.value,
            )
            return redirect(url_for("auth.auth"))

        # jwt token
        access_token = create_access_token(identity=email)
        response = redirect(url_for("index"))
        set_access_cookies(response, access_token)
        current_app.logger.info(
            "JWT created for user, id: %s, JWT: %s.", {user.id}, {access_token}
        )

        login_user(user, remember=True)
        current_app.logger.info("User logged in, id: %s.", {user.id})
        flash("You have been logged in.", FlashAlertTypeEnum.SUCCESS.value)

        return response

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "Register error in field %s: %s",
                    {getattr(form, field).label.text},
                    {error},
                )
        return render_template("auth.html", form=form)

    abort(HttpRequstEnum.METHOD_NOT_ALLOWED.value)


@auth_bp.route("/logout")
@login_required
def logout():
    """Log out the user."""

    current_app.logger.info("User logged out, id: %s.", {current_user.id})
    logout_user()
    flash("You have been logged out.", FlashAlertTypeEnum.SUCCESS.value)

    return redirect(url_for("auth.auth"))


@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    """Render the forgoet password page."""

    form = forms.ForgotPasswordForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            current_app.logger.error(
                "No user with that email exists, email: %s.", {form.email.data}
            )
            flash("No user with that email exists.", FlashAlertTypeEnum.DANGER.value)
            return redirect(url_for("auth.forgot_password"))

        if user.security_answer != form.security_answer.data:
            current_app.logger.error(
                "Invalid security answer, email: %s, security answer: %s.",
                {form.email.data},
                {form.security_answer.data},
            )
            flash("Invalid security answer.", FlashAlertTypeEnum.DANGER.value)
            return redirect(url_for("auth.forgot_password"))

        user.password = form.password.data

        # update user password
        db.session.commit()

        # send notification
        notice_event(user_id=user.id, notice_type=NoticeTypeEnum.USER_RESET_PASSWORD)

        current_app.logger.info("Password reset for user, id: %s.", {user.id})
        flash("Password has been reset.", FlashAlertTypeEnum.SUCCESS.value)
        return redirect(url_for("auth.auth"))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "Forgot password error in field %s: %s",
                    {getattr(form, field).label.text},
                    {error},
                )
        return redirect(url_for("auth.forgot_password"))

    return render_template("forgotPassword.html", form=form)


@auth_bp.route("/authorize/<provider>")
def authorize(provider: str):
    """Redirect to provider's OAuth2 login page."""

    if not current_user.is_anonymous:
        current_app.logger.info("User is already logged in, id: %s.", {current_user.id})
        return redirect(url_for("index"))

    provider_data = current_app.config[OAUTH2_PROVIDERS].get(provider)
    if provider_data is None:
        current_app.logger.error("Provider not found: %s.", {provider})
        abort(404)

    session[OAUTH2_STATE] = secrets.token_urlsafe(16)

    qs = urlencode(
        {
            "client_id": provider_data[CLIENT_ID],
            "redirect_uri": provider_data[CALLBACK_URL],
            "response_type": RESPONSE_TYPE,
            "scope": " ".join(provider_data[SCOPES]),
            "state": session[OAUTH2_STATE],
        }
    )
    return redirect(provider_data[AUTHORIZE_URL] + "?" + qs)


@auth_bp.route("/callback/<provider>")
def callback(provider: str):
    """Receive authorization code from provider and get user info."""

    provider_data = current_app.config[OAUTH2_PROVIDERS].get(provider)

    # get token from provider
    response = requests.post(
        provider_data[TOKEN_URL],
        data={
            "client_id": provider_data[CLIENT_ID],
            "client_secret": provider_data[CLIENT_SECRET],
            "code": request.args[RESPONSE_TYPE],
            "grant_type": AUTHORIZATION_CODE,
            "redirect_uri": url_for("auth.callback", provider=provider, _external=True),
        },
        headers={"Accept": "application/json"},
        timeout=30,
    )

    if response.status_code != 200:
        current_app.logger.error(
            "Failed to get token from provider: %s, status code: %s.",
            {provider},
            {response.status_code},
        )
        abort(401)

    oauth2_token = response.json().get("access_token")
    if not oauth2_token:
        current_app.logger.error("Failed to get token from provider: %s.", {provider})
        abort(401)

    # get user info from provider
    response = requests.get(
        provider_data["userinfo"]["url"],
        headers={
            "Authorization": "Bearer " + oauth2_token,
            "Accept": "application/json",
        },
        timeout=30,
    )
    user_info = response.json()

    if provider == OAuthProviderEnum.GOOGLE.value:
        username = user_info.get("name")
        email = user_info.get("email")
        avatar = user_info.get("picture")
    elif provider == OAuthProviderEnum.GITHUB.value:
        username = user_info.get("login")
        email = user_info.get("email")
        avatar = user_info.get("avatar_url")

    user = db.session.scalar(db.select(User).where(User.email == email))

    if user is None:
        user = User(
            username=username,
            email=email,
            avatar_url=avatar,
            use_google=provider == OAuthProviderEnum.GOOGLE.value,
            use_github=provider == OAuthProviderEnum.GITHUB.value,
            security_question="",
            security_answer="",
        )
        db.session.add(user)
        db.session.commit()
    else:
        if not user.use_google and provider == OAuthProviderEnum.GOOGLE.value:
            user.use_google = True
        if not user.use_github and provider == OAuthProviderEnum.GITHUB.value:
            user.use_github = True
        user.username = username
        user.avatar_url = avatar
        db.session.commit()

    login_user(user, remember=True)
    current_app.logger.info(
        "User logged in with %s, id: %s.", {provider}, {current_user.id}
    )
    flash("You have been logged in.", FlashAlertTypeEnum.SUCCESS.value)
    return redirect(url_for("index"))
