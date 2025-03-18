"""Main application module."""

import logging
import os
import uuid
from datetime import timedelta
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, g, render_template, request
from flask_login import current_user, login_required

from app.api.service import (
    communities_service,
    community_options_service,
    populars_service,
    posts_service,
    stats_service,
    user_stats_service,
    users_notices_service,
)
from app.constants import (
    AUTH_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    COMMUNITY_OPTION_NUM,
    G_NOTICE,
    G_NOTICE_NUM,
    G_POST_STAT,
    G_USER,
    POPULAR_POST_NUM,
    REDIRECT_URI,
    SCOPES,
    TOKEN_URL,
    USER_INFO_URL,
    EnvironmentEnum,
    HttpRequestEnum,
)
from app.models.user_notice import UserNotice
from app.swagger import get_swagger_config

from .api import api_bp
from .auth import auth_bp
from .community import community_bp
from .extensions import bcrypt, db, jwt, login_manager, scheduler, swag
from .job import job_bp
from .popular import popular_bp
from .post import post_bp
from .search import search_bp
from .user import user_bp
from .utils import get_config, get_env, get_pagination_details


def create_app(test_config: dict = None) -> Flask:
    """Create the Flask application."""

    app = Flask(__name__)

    # env
    env = get_env()

    # configuration
    if test_config is not None:
        app.config.update(test_config)
    else:
        init_config(app, env)

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
    @app.route("/", methods=["GET"])
    @login_required
    def index():

        # request args
        community_id = request.args.get("community_id", default=None, type=int)

        # community
        communities = get_home_communities()

        # post
        post_result = get_home_posts(community_id)
        posts = post_result["posts"]

        # pagination
        post_pagination = post_result["pagination"]
        pagination = get_pagination_details(
            current_page=post_pagination["page"],
            total_pages=post_pagination["total_pages"],
            total_items=post_pagination["total_items"],
        )

        # popular
        populars = get_home_populars()

        # stat
        stats = get_home_stats()

        # options
        community_options = get_home_community_options()

        return render_template(
            "index.html",
            render_id="index-posts",
            render_url="/index_posts",
            community_id=community_id,
            communities=communities,
            posts=posts,
            pagination=pagination,
            populars=populars,
            stats=stats,
            community_options=community_options,
        )

    @app.route("/index_posts", methods=["GET"])
    @login_required
    def index_posts():

        # post
        community_id = request.args.get("community_id")
        order_by = request.args.get("order_by")
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        post_result = get_home_posts(community_id, order_by, page, per_page)
        posts = post_result["posts"]

        # pagination
        post_pagination = post_result["pagination"]
        pagination = get_pagination_details(
            current_page=post_pagination["page"],
            total_pages=post_pagination["total_pages"],
            total_items=post_pagination["total_items"],
        )

        return render_template(
            "indexPost.html",
            community_id=community_id,
            posts=posts,
            pagination=pagination,
        )

    @app.route("/navbar", methods=["GET"])
    @login_required
    def navbar():
        return render_template("components/layout/navBar.html")

    @app.route("/notifications", methods=["GET"])
    @login_required
    def notification():
        notices = (
            users_notices_service(status="unread")
            .json.get("data")
            .get("user_notifications")
        )

        return render_template(
            "components/layout/navNotification.html", notices=notices
        )

    return app


def init_config(app: Flask, env: str) -> None:
    """Initialize application configuration."""

    app.config["SECRET_KEY"] = get_config("APP", "SECRET_KEY")
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
    app.config["SQLALCHEMY_DATABASE_URI"] = get_config("POSTGRESQL", "DATABASE_URL")
    app.config["OAUTH2_PROVIDERS"] = get_oauth2_config()
    app.config["SWAGGER"] = get_swagger_config()

    # Session configuration
    app.config["SESSION_COOKIE_SECURE"] = env == EnvironmentEnum.PROD.value
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Required for OAuth redirects
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
    app.config["SESSION_COOKIE_NAME"] = "askify_session"
    app.config["SESSION_TYPE"] = "filesystem"

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = get_config("APP", "JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = env == EnvironmentEnum.PROD.value
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/auth/refresh"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_COOKIE_SAMESITE"] = "Strict"
    app.config["JWT_ACCESS_CSRF_HEADER_NAME"] = "X-CSRF-TOKEN"
    app.config["JWT_REFRESH_CSRF_HEADER_NAME"] = "X-CSRF-TOKEN"
    app.config["JWT_CSRF_IN_COOKIES"] = True
    app.config["JWT_CSRF_METHODS"] = ["POST", "PUT", "PATCH", "DELETE"]


def init_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    scheduler.init_app(app)
    jwt.init_app(app)
    swag.init_app(app)


def register_blueprints(app: Flask) -> None:
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
    app.register_blueprint(job_bp)


def register_error_handlers(app: Flask) -> None:
    """Registers error handlers for common HTTP error codes."""

    @app.errorhandler(HttpRequestEnum.BAD_REQUEST.value)
    def bad_request_error(_):
        return render_template("errors/400.html"), HttpRequestEnum.BAD_REQUEST.value

    @app.errorhandler(HttpRequestEnum.UNAUTHORIZED.value)
    def unauthorized_error(_):
        return render_template("errors/401.html"), HttpRequestEnum.UNAUTHORIZED.value

    @app.errorhandler(HttpRequestEnum.FORBIDDEN.value)
    def forbidden_error(_):
        return render_template("errors/403.html"), HttpRequestEnum.FORBIDDEN.value

    @app.errorhandler(HttpRequestEnum.NOT_FOUND.value)
    def page_not_found_error(_):
        return render_template("errors/404.html"), HttpRequestEnum.NOT_FOUND.value

    @app.errorhandler(HttpRequestEnum.METHOD_NOT_ALLOWED.value)
    def method_not_allowed_error(_):
        return (
            render_template("errors/405.html"),
            HttpRequestEnum.METHOD_NOT_ALLOWED.value,
        )

    @app.errorhandler(HttpRequestEnum.INTERNAL_SERVER_ERROR.value)
    def internal_server_error(_):
        # pylint: disable=no-member
        db.session.rollback()
        return (
            render_template("errors/500.html"),
            HttpRequestEnum.INTERNAL_SERVER_ERROR.value,
        )


def register_logging(app: Flask) -> None:
    """Register logging for the application."""

    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = TimedRotatingFileHandler(
        "logs/askify.log", when="D", interval=1, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)


def register_middleware(app: Flask) -> None:
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


def register_context_processors(app: Flask) -> None:
    """Register context processors for the application."""

    # global context processors, to set global variables for all templates
    @app.context_processor
    def inject_user():
        return {G_USER: current_user}

    @app.context_processor
    def inject_post_stat():
        if current_user.is_authenticated:
            stats_data = user_stats_service().json
            post_num = stats_data["data"]["user_stats"]["request_num"]

            return {G_POST_STAT: post_num}

        return {G_POST_STAT: 0}

    @app.context_processor
    def inject_notice_num():
        notice_num = 0
        if current_user.is_authenticated:
            notice_num = UserNotice.query.filter_by(
                user_id=current_user.id, status=False
            ).count()

        g.notice_num = notice_num
        return {G_NOTICE_NUM: g.notice_num}

    @app.context_processor
    def inject_notice():
        notices = []
        if current_user.is_authenticated:
            response = users_notices_service(status="unread").json
            data = response.get("data", {})
            notices = data.get("user_notifications", [])

        return {G_NOTICE: notices}


def get_oauth2_config() -> dict:
    """Get OAuth2 configuration."""
    return {
        "google": {
            "client_id": get_config("GOOGLE", "GOOGLE_OAUTH_CLIENT_ID"),
            "client_secret": get_config("GOOGLE", "GOOGLE_OAUTH_CLIENT_SECRET"),
            "redirect_uri": get_config("GOOGLE", "GOOGLE_OAUTH_REDIRECT_URI"),
            "authorize_url": get_config("GOOGLE", "GOOGLE_OAUTH_AUTH_URL"),
            "token_url": get_config("GOOGLE", "GOOGLE_OAUTH_TOKEN_URL"),
            "user_info": {
                "url": get_config("GOOGLE", "GOOGLE_OAUTH_USER_INFO_URL"),
                "email_key": "email",
                "name_key": "name",
                "picture_key": "picture",
            },
            "scopes": [
                get_config("GOOGLE", "GOOGLE_OAUTH_SCOPE_PROFILE"),
                get_config("GOOGLE", "GOOGLE_OAUTH_SCOPE_EMAIL"),
            ],
        },
        "github": {
            "client_id": get_config("GITHUB", "GITHUB_OAUTH_CLIENT_ID"),
            "client_secret": get_config("GITHUB", "GITHUB_OAUTH_CLIENT_SECRET"),
            "redirect_uri": get_config("GITHUB", "GITHUB_OAUTH_REDIRECT_URI"),
            "authorize_url": get_config("GITHUB", "GITHUB_OAUTH_AUTH_URL"),
            "token_url": get_config("GITHUB", "GITHUB_OAUTH_TOKEN_URL"),
            "user_info": {
                "url": get_config("GITHUB", "GITHUB_OAUTH_USER_INFO_URL"),
                "email_key": "email",
                "name_key": "name",
                "picture_key": "avatar_url",
            },
            "scopes": ["read:user", "user:email"],
        },
    }


def get_home_posts(
    community_id: int = None,
    order_by: str = "create_at_desc",
    page: int = 1,
    per_page: int = 10,
) -> list:
    """Get index post data."""

    posts_response = posts_service(community_id, order_by, page, per_page).json
    posts = posts_response.get("data").get("posts")
    pagination = posts_response.get("pagination")

    post_items = [
        {
            "id": post["id"],
            "title": post["title"],
            "author": post["author"]["username"],
            "tag": post["tag"]["name"],
            "reply_num": post["reply_num"],
            "view_num": post["view_num"],
            "like_num": post["like_num"],
            "save_num": post["save_num"],
            "create_at": post["create_at"],
        }
        for post in posts
    ]

    return {"posts": post_items, "pagination": pagination}


def get_home_populars() -> list:
    """Get index popular data."""

    populars_response = populars_service(POPULAR_POST_NUM).json
    populars = populars_response.get("data").get("populars")

    return [
        {
            "id": popular["request"]["id"],
            "title": popular["request"]["title"],
            "author": popular["author"]["username"],
            "avatar": popular["author"]["avatar_url"],
            "view_num": popular["view_num"],
            "reply_num": popular["reply_num"],
            "create_at": popular["request"]["create_at"],
        }
        for popular in populars
    ]


def get_home_stats() -> list:
    """Get index stats data."""

    stats_response = stats_service().json
    return stats_response.get("data").get("stats")


def get_home_communities() -> list:
    """Get index communities data."""

    communities_response = communities_service(per_page=COMMUNITY_OPTION_NUM).json
    communities = communities_response.get("data").get("communities")

    return [
        {"id": community["id"], "name": community["name"]} for community in communities
    ]


def get_home_community_options() -> list:
    """Get index community options data."""

    communities_response = community_options_service().json
    return communities_response.get("data").get("community_options")
