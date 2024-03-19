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
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import auth_bp
from app.constant import OAuthProviderEnum
from app.extensions import db, login_manager
from app.models.user import User

from ..auth import auth_bp
from . import service


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object."""
    return db.session.get(User, user_id)


@auth_bp.route("/authorize/<provider>")
def oauth2_authorize(provider):
    """Redirect to provider's OAuth2 login page."""
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)

    session["oauth2_state"] = secrets.token_urlsafe(16)

    qs = urlencode(
        {
            "client_id": provider_data["client_id"],
            "redirect_uri": url_for(
                "auth.oauth2_callback", provider=provider, _external=True
            ),
            "response_type": "code",
            "scope": " ".join(provider_data["scopes"]),
            "state": session["oauth2_state"],
        }
    )

    url = provider_data["authorize_url"] + "?" + qs
    print(url)

    return redirect(provider_data["authorize_url"] + "?" + qs)


@auth_bp.route("/callback/<provider>")
def oauth2_callback(provider):
    """Receive authorization code from provider and get user info."""
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)

    if "error" in request.args:
        for k, v in request.args.items():
            if k.startswith("error"):
                flash(f"{k}: {v}")
        return redirect(url_for("index"))

    if request.args["state"] != session.get("oauth2_state"):
        abort(401)

    if "code" not in request.args:
        abort(401)

    # get token from provider
    response = requests.post(
        provider_data["token_url"],
        data={
            "client_id": provider_data["client_id"],
            "client_secret": provider_data["client_secret"],
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": url_for(
                "auth.oauth2_callback", provider=provider, _external=True
            ),
        },
        headers={"Accept": "application/json"},
        timeout=30,
    )

    if response.status_code != 200:
        abort(401)

    oauth2_token = response.json().get("access_token")
    if not oauth2_token:
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
    print(f"user_info Response: {user_info}")

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
            authenticated=True,
            use_google=True if provider == OAuthProviderEnum.GOOGLE.value else False,
            use_github=True if provider == OAuthProviderEnum.GITHUB.value else False,
        )
        db.session.add(user)
        db.session.commit()
    else:
        if not user.use_google and provider == OAuthProviderEnum.GOOGLE.value:
            user.use_google = True
        if not user.use_github and provider == OAuthProviderEnum.GITHUB.value:
            user.use_github = True
        db.session.commit()

    login_user(user)
    return render_template("auth.html", alert_message="You are now logged in.")


@auth_bp.route("/auth")
def auth():
    """Render the auth page."""
    return render_template("auth.html")


@auth_bp.route("/login", methods=["POST"])
def login():
    """Log in the user."""
    #  user = User(
    #         username=username,
    #         email=email,
    #         avatar_url=avatar,
    #         authenticated=True,
    #         use_google=True if provider == OAuthProviderEnum.GOOGLE.value else False,
    #         use_github=True if provider == OAuthProviderEnum.GITHUB.value else False,
    #     )
    #     db.session.add(user)
    #     db.session.commit()
    # return auth.login(username, password)
    return "login"


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    form = service.RegisterForm(request.form)
    user = User(
        username=request.form["registerUsername"],
        email=request.form["registerEmail"],
        password=request.form["registerRepeatPassword"],
        avatar_url="",
        authenticated=True,
        use_google=False,
        use_github=False,
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("index"))


@auth_bp.route("/logout")
@login_required
def logout():
    """Log out the user."""
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))


@auth_bp.route("/forgot-password")
def forgot_password():
    """Render the forgot password page."""
    return "forgot-password"
