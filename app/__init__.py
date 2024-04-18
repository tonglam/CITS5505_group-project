"""Main application module."""

import logging

from flask import Flask, render_template, request
from flask_login import current_user, login_required

from .api import api_bp
from .auth import auth_bp
from .community import community_bp
from .errors import register_error_handlers
from .extensions import bcrypt, db, login_manager, migrate, scheduler
from .logs import configure_logging
from .notice import notice_bp
from .popular import popular_bp
from .post import post_bp
from .search import search_bp
from .user import user_bp
from .utils import get_config


def create_app():
    """Create the Flask application."""
    app = Flask(__name__)

    app.config["SECRET_KEY"] = get_config("APP", "SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_config("SQLITE", "DATABASE_URL")
    app.config["OAUTH2_PROVIDERS"] = get_oauth2_config()

    # extensions
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # scheduled tasks
    scheduler.init_app(app)

    # blueprints
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(
        auth_bp,
        static_url_path="/auth/static",
    )
    app.register_blueprint(
        search_bp,
        static_url_path="/search/static",
    )
    app.register_blueprint(
        notice_bp,
        static_url_path="/notice/static",
    )
    app.register_blueprint(
        post_bp,
        url_prefix="/posts",
        static_url_path="/post/static",
    )
    app.register_blueprint(
        popular_bp,
        url_prefix="/populars",
        static_url_path="/populars/static",
    )
    app.register_blueprint(
        community_bp,
        url_prefix="/communities",
        static_url_path="/communities/static",
    )
    app.register_blueprint(
        user_bp,
        url_prefix="/users",
        static_url_path="/users/static",
    )
    # error init
    register_error_handlers(app)
    # log init
    configure_logging(app)

    @app.route("/")
    @login_required
    def index():
        return render_template("index.html")

    @app.before_request
    def log_request_info():
        app.logger.info("Request: %s %s", request.method, request.url)
        app.logger.info("Request Headers: %s", request.headers)
        app.logger.info("Request Body: %s", request.get_data())

    @app.after_request
    def log_response_info(response):
        app.logger.info("Response: %s", response.status)
        return response

    @app.context_processor
    def inject_user():
        return {"user": current_user}

    return app


def get_oauth2_config():
    """Get OAuth2 configuration."""
    return {
        "google": {
            "client_id": get_config("GOOGLE", "CLIENT_ID"),
            "client_secret": get_config("GOOGLE", "CLIENT_SECRET"),
            "callback_url": get_config("GOOGLE", "CALLBACK_URL"),
            "authorize_url": get_config("GOOGLE", "AUTHORIZE_URL"),
            "token_url": get_config("GOOGLE", "TOKEN_URL"),
            "userinfo": {
                "url": get_config("GOOGLE", "USER_URL"),
                "email": lambda json: json["email"],
            },
            "scopes": [
                get_config("GOOGLE", "SCOPES_PROFILE"),
                get_config("GOOGLE", "SCOPES_EMAIL"),
            ],
        },
        "github": {
            "client_id": get_config("GITHUB", "CLIENT_ID"),
            "client_secret": get_config("GITHUB", "CLIENT_SECRET"),
            "callback_url": get_config("GITHUB", "CALLBACK_URL"),
            "authorize_url": get_config("GITHUB", "AUTHORIZE_URL"),
            "token_url": get_config("GITHUB", "TOKEN_URL"),
            "userinfo": {
                "url": get_config("GITHUB", "USER_URL"),
                "email": lambda json: json[0]["email"],
            },
            "scopes": ["user"],
        },
    }
