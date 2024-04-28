"""Main application module."""

import uuid

from flask import Flask, g, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import func
from app.models.request import Request

from app.constants import G_NOTICE_NUM, G_USER
from app.models.notice import Notice

from .api import api_bp
from .auth import auth_bp
from .community import community_bp
from .errors import register_error_handlers
from .extensions import bcrypt, db, jwt, login_manager, migrate, scheduler
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

    # app configuration
    app.config["SECRET_KEY"] = get_config("APP", "SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_config("SQLITE", "DATABASE_URL")
    app.config["OAUTH2_PROVIDERS"] = get_oauth2_config()
    app.config["BASE_URL"] = get_config("APP", "BASE_URL")
    app.config["JWT_SECRET_KEY"] = get_config("APP", "JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True

    # extensions
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)
    jwt.init_app(app)

    # blueprints
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

    # register error handlers
    register_error_handlers(app)

    # register logging
    configure_logging(app)

    # home page
    @app.route("/")
    @login_required
    def index():
        random_requests = Request.query.order_by(func.random()).limit(10).all()  # pylint: disable=not-callable
        return render_template('index.html', requests=random_requests)

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
