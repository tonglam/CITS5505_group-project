"""Main application module."""

import logging
import os
import uuid
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, g, render_template, request
from flask_login import current_user, login_required

from app.constants import G_NOTICE_NUM, G_USER, EnvironmentEnum, HttpRequstEnum
from app.models.notice import Notice
from app.swagger import get_swagger_config

from .api import api_bp
from .auth import auth_bp
from .community import community_bp
from .extensions import bcrypt, db, jwt, login_manager, migrate, scheduler, swag
from .notice import notice_bp
from .popular import popular_bp
from .post import post_bp
from .search import search_bp
from .user import user_bp
from .utils import get_config, get_env


def create_app():
    """Create the Flask application."""

    app = Flask(__name__)

    # configuration
    init_config(app)

    # extensions
    init_extensions(app)

    # blueprints
    register_blueprints(app)

    # error handlers
    register_error_handlers(app)

    # logging
    register_logging(app)

    # middleware
    register_middleware(app)

    # global context processors
    register_context_processors(app)

    # home page
    @app.route("/")
    @login_required
    def index():
        return render_template("index.html")

    return app


def init_config(app):
    """Initialize application configuration."""

    app.config["SECRET_KEY"] = get_config("APP", "SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_config("SQLITE", "DATABASE_URL")
    app.config["OAUTH2_PROVIDERS"] = get_oauth2_config()
    app.config["SWAGGER"] = get_swagger_config()
    app.config["JWT_SECRET_KEY"] = get_config("APP", "JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = get_env() == EnvironmentEnum.PROD.value
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/auth/refresh"


def init_extensions(app):
    """Initialize Flask extensions."""

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)
    jwt.init_app(app)
    swag.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(
        auth_bp,
        url_prefix="/auth",
        static_url_path="/auth/static",
    )
    app.register_blueprint(
        search_bp,
        url_prefix="/search",
        static_url_path="/search/static",
    )
    app.register_blueprint(
        notice_bp,
        url_prefix="/notifications",
        static_url_path="/notifications/static",
    )
    app.register_blueprint(
        post_bp,
        url_prefix="/posts",
        static_url_path="/posts/static",
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


def register_error_handlers(app):
    """Registers error handlers for common HTTP error codes."""

    @app.errorhandler(HttpRequstEnum.BAD_REQUEST.value)
    def bad_request_error(_):
        return render_template("errors/400.html"), HttpRequstEnum.BAD_REQUEST.value

    @app.errorhandler(HttpRequstEnum.UNAUTHORIZED.value)
    def unauthorized_error(_):
        return render_template("errors/401.html"), HttpRequstEnum.UNAUTHORIZED.value

    @app.errorhandler(HttpRequstEnum.FORBIDDEN.value)
    def forbidden_error(_):
        return render_template("errors/403.html"), HttpRequstEnum.FORBIDDEN.value

    @app.errorhandler(HttpRequstEnum.NOT_FOUND.value)
    def page_not_found_error(_):
        return render_template("errors/404.html"), HttpRequstEnum.NOT_FOUND.value

    @app.errorhandler(HttpRequstEnum.METHOD_NOT_ALLOWED.value)
    def method_not_allowed_error(_):
        return (
            render_template("errors/405.html"),
            HttpRequstEnum.METHOD_NOT_ALLOWED.value,
        )

    @app.errorhandler(HttpRequstEnum.INTERNAL_SERVER_ERROR.value)
    def internal_server_error(_):
        db.session.rollback()
        return (
            render_template("errors/500.html"),
            HttpRequstEnum.INTERNAL_SERVER_ERROR.value,
        )


def register_logging(app):
    """log config"""

    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = TimedRotatingFileHandler(
        "logs/application.log", when="D", interval=1, backupCount=30
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    )
    file_handler.setLevel(logging.DEBUG)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)

    app.logger.info("Application startup")


def register_middleware(app):
    """Register middleware for the application."""

    # logging middleware for http request and response
    @app.before_request
    def before_request():
        if request.url.endswith(".css") or request.url.endswith(".js"):
            return

        g.request_uuid = str(uuid.uuid4())
        g.request_body = request.get_data(as_text=True) if request.data else None
        app.logger.info(
            "[%s] Request [%s]: %s %s",
            g.request_uuid,
            request.method,
            request.url,
            request.headers,
        )
        request_body = g.request_body
        if request_body:
            app.logger.info("[%s] Request Body: %s", g.request_uuid, g.request_body)

    @app.after_request
    def after_request(response):
        content_type = response.content_type
        request_uuid = g.request_uuid if hasattr(g, "request_uuid") else ""

        if (
            "html" in content_type
            or "css" in content_type
            or "javascript" in content_type
        ):
            app.logger.info(
                "[%s] Response [%s]: Status %s, Headers %s",
                request_uuid,
                request.method,
                response.status,
                response.headers,
            )
        elif "application/json" in content_type:
            app.logger.info(
                "[%s] Response [%s]: Status %s, Headers %s",
                request_uuid,
                request.method,
                response.status,
                response.headers,
            )
            response_body = response.get_data(as_text=True)
            if response_body:
                app.logger.info("[%s] Response Body: %s", request_uuid, response_body)

        return response


def register_context_processors(app):
    """Register context processors for the application."""

    # global context processors, to set global variables for all templates
    @app.context_processor
    def inject_user():
        return {G_USER: current_user}

    @app.context_processor
    def inject_notice_num():
        if current_user.is_authenticated:
            notice_num = Notice.query.filter_by(
                user=current_user.id, status=False
            ).count()
        else:
            notice_num = 0

        g.notice_num = notice_num

        return {G_NOTICE_NUM: g.notice_num}


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
