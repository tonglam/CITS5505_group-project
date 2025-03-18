"""Routes for authentication."""

import secrets
from datetime import timedelta
from urllib.parse import urlencode

import requests
from flask import (
    abort,
    current_app,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf.csrf import generate_csrf

from app.auth import auth_bp, forms
from app.constants import (
    OAUTH2_PROVIDERS,
    OAUTH2_STATE,
    RESPONSE_TYPE,
    FlashAlertTypeEnum,
    HttpRequestEnum,
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
                flash(
                    f"{getattr(form, field).label.text}, {error}",
                    FlashAlertTypeEnum.DANGER.value,
                )

        return redirect(url_for("auth.auth"))

    abort(HttpRequestEnum.METHOD_NOT_ALLOWED.value)


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

        # Log in the user with Flask-Login
        login_user(user, remember=True)
        current_app.logger.info("User logged in, id: %s.", {user.id})

        try:
            # Create JWT tokens with proper expiration
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(
                    hours=5
                ),  # 5 hours expiration to match app config
            )
            refresh_token = create_refresh_token(
                identity=user.id, expires_delta=timedelta(days=30)  # 30 days expiration
            )

            # Create response
            response = redirect(url_for("index"))

            # Set JWT cookies with secure flags
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            current_app.logger.info("JWT tokens created for user, id: %s", {user.id})

            # Set CSRF token with secure flags
            csrf_token = generate_csrf()
            response.set_cookie(
                "csrf_token", csrf_token, httponly=True, secure=True, samesite="Strict"
            )
            current_app.logger.info("CSRF token created for user, id: %s.", {user.id})

            flash("You have been logged in.", FlashAlertTypeEnum.SUCCESS.value)
            return response

        except (RuntimeError, ValueError) as e:
            current_app.logger.error(
                "Error creating tokens for user %s: %s", {user.id}, {str(e)}
            )
            flash(
                "Error during login process. Please try again.",
                FlashAlertTypeEnum.DANGER.value,
            )
            return redirect(url_for("auth.auth"))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "Login error in field %s: %s",
                    {getattr(form, field).label.text},
                    {error},
                )
                flash(
                    f"{getattr(form, field).label.text}, {error}",
                    FlashAlertTypeEnum.DANGER.value,
                )
        return redirect(url_for("auth.auth"))

    abort(HttpRequestEnum.METHOD_NOT_ALLOWED.value)


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    """Log out the user."""

    current_app.logger.info("User logged out, id: %s.", {current_user.id})
    logout_user()

    # jwt token
    response = redirect(url_for("auth.auth"))
    unset_jwt_cookies(response)

    flash("You have been logged out.", FlashAlertTypeEnum.SUCCESS.value)

    return response


@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    """Render the forgot password page."""

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
        current_app.logger.info(
            "User password updated, email: %s, id: %s.", {user.email}, {user.id}
        )

        # send notification
        notice_event(notice_type=NoticeTypeEnum.USER_RESET_PASSWORD)

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
                flash(
                    f"{getattr(form, field).label.text}, {error}",
                    FlashAlertTypeEnum.DANGER.value,
                )
        return redirect(url_for("auth.forgot_password"))

    return render_template("forgotPassword.html", form=form)


@auth_bp.route("/authorize/<provider>", methods=["GET"])
def authorize(provider: str):
    """Redirect to provider's OAuth2 login page."""
    current_app.logger.debug("Starting OAuth authorization for provider: %s", provider)

    if not current_user.is_anonymous:
        current_app.logger.info("User is already logged in, id: %s.", {current_user.id})
        return redirect(url_for("index"))

    provider_data = current_app.config[OAUTH2_PROVIDERS].get(provider)
    if provider_data is None:
        current_app.logger.error("Provider not found: %s.", {provider})
        abort(404)

    current_app.logger.debug("Provider data: %s", provider_data)
    session[OAUTH2_STATE] = secrets.token_urlsafe(16)
    current_app.logger.debug("Generated state: %s", session[OAUTH2_STATE])

    qs = urlencode(
        {
            "client_id": provider_data["client_id"],
            "redirect_uri": provider_data["redirect_uri"],
            "response_type": RESPONSE_TYPE,
            "scope": " ".join(provider_data["scopes"]),
            "state": session[OAUTH2_STATE],
        }
    )
    auth_url = provider_data["authorize_url"] + "?" + qs
    current_app.logger.debug("Redirecting to auth URL: %s", auth_url)
    return redirect(auth_url)


def _get_oauth_token(provider: str, code: str) -> dict:
    """Get OAuth token from provider."""
    try:
        current_app.logger.debug(
            "Getting OAuth token for provider %s with code %s", provider, code
        )
        provider_data = current_app.config[OAUTH2_PROVIDERS][provider]
        token_url = provider_data["token_url"]
        client_id = provider_data["client_id"]
        client_secret = provider_data["client_secret"]
        redirect_uri = provider_data["redirect_uri"]

        token_params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",  # Required for both GitHub and Google
        }

        headers = {"Accept": "application/json"}

        if provider == OAuthProviderEnum.GITHUB.value:
            token_params["grant_type"] = "authorization_code"

        current_app.logger.debug("Token request to URL: %s", token_url)
        current_app.logger.debug("Token request params: %s", token_params)
        current_app.logger.debug("Token request headers: %s", headers)

        token_response = requests.post(
            token_url, data=token_params, headers=headers, timeout=30
        )
        current_app.logger.debug(
            "Token response status: %s", token_response.status_code
        )
        current_app.logger.debug("Token response content: %s", token_response.text)

        token_response.raise_for_status()

        response_data = token_response.json()
        if provider == OAuthProviderEnum.GITHUB.value and "error" in response_data:
            raise ValueError(f"GitHub OAuth error: {response_data['error']}")

        return response_data
    except requests.RequestException as e:
        current_app.logger.error("Failed to get OAuth token: %s", str(e))
        raise ValueError("Failed to get OAuth token") from e


def _get_user_info(provider: str, access_token: str) -> dict:
    """Get user info from provider."""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        if provider == OAuthProviderEnum.GITHUB.value:
            # First get user profile
            user_response = requests.get(
                "https://api.github.com/user", headers=headers, timeout=30
            )
            user_response.raise_for_status()
            user_data = user_response.json()

            # Then get user email if not present
            if not user_data.get("email"):
                email_response = requests.get(
                    "https://api.github.com/user/emails", headers=headers, timeout=30
                )
                email_response.raise_for_status()
                emails = email_response.json()
                primary_email = next(
                    (email["email"] for email in emails if email["primary"]), None
                )
                if primary_email:
                    user_data["email"] = primary_email

            return user_data

        # Google
        user_response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers=headers,
            timeout=30,
        )
        user_response.raise_for_status()
        return user_response.json()

    except requests.RequestException as e:
        current_app.logger.error("Failed to get user info: %s", str(e))
        raise ValueError("Failed to get user info") from e


@auth_bp.route("/callback/<provider>", methods=["GET"])
def callback(provider: str):
    """Handle the OAuth callback."""
    current_app.logger.debug("OAuth callback received for provider: %s", provider)

    # Check if provider exists in config
    providers = current_app.config.get(OAUTH2_PROVIDERS)
    if not providers or provider not in providers:
        current_app.logger.error(
            "Provider %s not found in OAUTH2_PROVIDERS config: %s", provider, providers
        )
        abort(HttpRequestEnum.NOT_FOUND.value)

    # Verify state to prevent CSRF
    state = request.args.get("state")
    stored_state = session.get(OAUTH2_STATE)
    current_app.logger.debug(
        "Comparing states - Received: %s, Stored: %s", state, stored_state
    )

    if state != stored_state:
        current_app.logger.error(
            "Invalid state parameter. Received: %s, Expected: %s", state, stored_state
        )
        flash("Invalid state parameter.", FlashAlertTypeEnum.DANGER.value)
        return redirect(url_for("auth.auth"))

    code = request.args.get("code")
    if not code:
        current_app.logger.error("No code parameter")
        flash("Authentication failed.", FlashAlertTypeEnum.DANGER.value)
        return redirect(url_for("auth.auth"))

    try:
        # Get OAuth token
        token_data = _get_oauth_token(provider, code)
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("No access token in response")

        # Get user info
        user_info = _get_user_info(provider, access_token)

        # Process user info
        email = user_info.get("email")
        if not email:
            raise ValueError("No email in user info")

        # Find or create user
        user = User.query.filter_by(email=email).first()
        if not user:
            username = user_info.get("name", "").split()[0]
            avatar_url = user_info.get("avatar_url") or user_info.get("picture")

            user = User(
                username=username,
                email=email,
                avatar_url=avatar_url,
                use_google=provider == OAuthProviderEnum.GOOGLE.value,
                use_github=provider == OAuthProviderEnum.GITHUB.value,
                security_question="",  # Default empty for OAuth users
                security_answer="",  # Default empty for OAuth users
            )
            db.session.add(user)
            db.session.commit()

        # Update OAuth flags
        if provider == OAuthProviderEnum.GOOGLE.value:
            user.use_google = True
        else:
            user.use_github = True
        db.session.commit()

        # Log in user
        login_user(user, remember=True)
        current_app.logger.info("User logged in with %s, id: %s", provider, user.id)

        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response = redirect(url_for("index"))
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        flash(
            f"Successfully logged in with {provider}.", FlashAlertTypeEnum.SUCCESS.value
        )
        return response

    except (ValueError, requests.RequestException) as e:
        current_app.logger.error("OAuth callback error: %s", str(e))
        flash("Authentication failed.", FlashAlertTypeEnum.DANGER.value)
        return redirect(url_for("auth.auth"))


@auth_bp.route("/cookies", methods=["GET"])
def get_cookies():
    """Get all cookies."""
    cookies = {}
    for key, value in request.cookies.items():
        cookies[key] = value
    return jsonify(cookies)


@auth_bp.route("/test-jwt", methods=["GET"])
@login_required
def test_jwt():
    """Render the JWT test page."""
    response = make_response(render_template("test_jwt.html"))

    # Ensure CSRF token is set
    if "csrf_token" not in request.cookies:
        csrf = generate_csrf()
        response.set_cookie("csrf_token", csrf)

    return response


@auth_bp.route("/test-auth", methods=["GET"])
@jwt_required()
def test_auth():
    """Test endpoint for JWT authentication."""
    current_identity = get_jwt_identity()
    user = User.query.get(current_identity)
    if not user:
        return jsonify({"message": "User not found", "status": "error"}), 404

    return jsonify(
        {
            "message": "Protected endpoint accessed successfully",
            "user_id": current_identity,
            "username": user.username,
            "status": "success",
        }
    )


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)

        response = jsonify({"msg": "Token refreshed successfully"})
        set_access_cookies(response, access_token)

        return response
    except (RuntimeError, ValueError) as e:
        current_app.logger.error("Token refresh error: %s", str(e))
        return jsonify({"msg": "Token refresh failed"}), 401


@auth_bp.route("/force-expire", methods=["POST"])
@login_required
def force_expire():
    """Force expire the user's tokens."""
    try:
        response = jsonify({"msg": "Tokens expired"})
        unset_jwt_cookies(response)
        return response
    except (RuntimeError, ValueError) as e:
        current_app.logger.error("Force expire error: %s", str(e))
        return jsonify({"msg": "Failed to expire tokens"}), 500


@auth_bp.route("/debug-jwt", methods=["GET"])
@jwt_required()
def debug_jwt():
    """Debug JWT tokens."""
    headers = dict(request.headers.items())
    cookies = dict(request.cookies.items())

    return jsonify(
        {
            "headers": headers,
            "cookies": cookies,
            "current_user": current_user.to_dict() if current_user else None,
        }
    )
