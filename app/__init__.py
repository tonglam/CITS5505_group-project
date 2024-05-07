"""Main application module."""

import logging
import os
import uuid
from logging.handlers import TimedRotatingFileHandler

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from flask import Flask, g, render_template, request
from flask_login import current_user, login_required
from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)
from sqlalchemy.sql import text

from app.api.service import (
    communities_service,
    populars_service,
    posts_service,
    stats_service,
)
from app.constants import (
    G_NOTICE_NUM,
    G_POST_STAT,
    G_USER,
    POPULAR_POST_NUM,
    EnvironmentEnum,
    HttpRequestEnum,
)
from app.models.user_notice import UserNotice
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
from .utils import get_config, get_env, get_pagination_details


def create_app() -> Flask:
    """Create the Flask application."""

    app = Flask(__name__)

    # env
    env = get_env()

    # configuration
    init_config(app, env)

    # extensions
    init_extensions(app)

    # init dev db
    init_dev_db(app, env)

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
        # community
        communities = get_home_communities()

        # post
        post_result = get_home_posts()
        posts = post_result["posts"]

        # pagination
        post_pagination = post_result["pagination"]
        pagination = get_pagination_details(
            current_page=post_pagination["page"],
            total_pages=post_pagination["total_pages"],
        )

        # popular
        populars = get_home_populars()

        # stat
        stats = get_home_stats()

        return render_template(
            "index.html",
            render_id="index-posts",
            render_url="/index_posts",
            communities=communities,
            posts=posts,
            pagination=pagination,
            populars=populars,
            stats=stats,
        )

    @app.route("/index_posts")
    @login_required
    def index_posts():

        # post
        community_id = request.args.get("community_id")
        order_by = request.args.get("order_by")
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        print("community_id: ", community_id)
        print("order_by: ", order_by)
        print("page: ", page)
        print("per_page: ", per_page)

        post_result = get_home_posts(community_id, order_by, page, per_page)
        posts = post_result["posts"]

        # pagination
        post_pagination = post_result["pagination"]
        pagination = get_pagination_details(
            current_page=post_pagination["page"],
            total_pages=post_pagination["total_pages"],
        )
        print("pagination: ", pagination)

        return render_template(
            "indexPost.html",
            posts=posts,
            pagination=pagination,
        )

    return app


def init_config(app: Flask, env: str) -> None:
    """Initialize application configuration."""

    app.config["SECRET_KEY"] = get_config("APP", "SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_config("SQLITE", "DATABASE_URL")
    app.config["OAUTH2_PROVIDERS"] = get_oauth2_config()
    app.config["SWAGGER"] = get_swagger_config()
    app.config["JWT_SECRET_KEY"] = get_config("APP", "JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = env == EnvironmentEnum.PROD.value
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/auth/refresh"


def init_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)
    jwt.init_app(app)
    swag.init_app(app)


def init_dev_db(app: Flask, env: str) -> None:
    """Init the development database."""

    # only apply on dev environment
    if env != EnvironmentEnum.DEV.value:
        app.logger.info(
            "Current environment is %s. Skip development database init.", env
        )
        return

    # check if db file exists
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    db_file = f"instance/{uri.split('sqlite:///')[1]}"

    alembic_file = "migrations/alembic.ini"
    alembic_cfg = Config(alembic_file)

    with app.app_context():
        if not os.path.exists(db_file):
            # create if not exists
            app.logger.info("Development database does not exist. Creating...")
            create_dev_db(app, db_file)
            app.logger.info("Development database created.")

            # set migration version to head
            command.stamp(alembic_cfg, "head")

        else:
            # check if migrations exists
            if not os.path.exists(alembic_file):
                app.logger.info("Database Migrations does not exist.")
                return

            # execute migrations
            app.logger.info(
                "Development database already exists. Checking migrations..."
            )
            migrate_dev_db(app, alembic_cfg)

        app.logger.info("Development database ready.")


def create_dev_db(app: Flask, db_file: str) -> None:
    """Create the development database."""

    try:
        db.drop_all()
        db.create_all()
        app.logger.info("Development database created.")

        # execute backup sql
        with open("sql/dev.backup.sql", "r", encoding="utf-8") as f:
            sql_commands = f.read().split(";")
            for sql_command in sql_commands:
                if sql_command.strip():
                    execute_raw_sql(app=app, query=sql_command)
        app.logger.info("Development backup sql executed.")
    except (
        IOError,
        IntegrityError,
        OperationalError,
        ProgrammingError,
        SQLAlchemyError,
    ) as db_err:
        app.logger.error(f"Database operation failed: {db_err}")
        if os.path.exists(db_file):
            os.remove(db_file)
        app.logger.info("Development database removed.")

        raise db_err


def execute_raw_sql(app: Flask, query: str, **params: dict) -> None:
    """Function to execute raw SQL queries."""

    with db.engine.connect() as connection:
        with connection.begin() as transaction:
            try:
                connection.execute(text(query), **params)
                transaction.commit()
            except (DataError, IntegrityError, OperationalError, ProgrammingError) as e:
                transaction.rollback()
                app.logger.error("Error occurred: %s", e)


def migrate_dev_db(app: Flask, alembic_cfg: Config) -> None:
    """Migrate the development database."""

    if check_dev_db_migration(app, alembic_cfg):
        app.logger.info("Development database needs to be migrated.")
        command.upgrade(alembic_cfg, "head")

    app.logger.info("Development database migrated.")


def check_dev_db_migration(app: Flask, alembic_cfg: Config) -> bool:
    """Check if the development database needs to be migrated."""

    with db.engine.connect() as connection:
        # current migration version
        context = MigrationContext.configure(connection)
        current_version = context.get_current_revision()
        app.logger.info("Current migration version: %s", current_version)

        # latest migration version
        last_version = get_latest_migration_version(alembic_cfg)
        app.logger.info("Latest migration version: %s", last_version)

        return current_version != last_version


def get_latest_migration_version(alembic_cfg: Config) -> str:
    """Get the latest migration version."""

    script = ScriptDirectory.from_config(alembic_cfg)
    heads = script.get_heads()
    return heads[0] if heads else None


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
        db.session.rollback()
        return (
            render_template("errors/500.html"),
            HttpRequestEnum.INTERNAL_SERVER_ERROR.value,
        )


def register_logging(app: Flask) -> None:
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
        stats_data = stats_service().json
        post_num = stats_data["data"]["stats"]["request_num"]

        return {G_POST_STAT: post_num}

    @app.context_processor
    def inject_notice_num():
        if current_user.is_authenticated:
            notice_num = UserNotice.query.filter_by(
                user=current_user, status=False
            ).count()
        else:
            notice_num = 0

        g.notice_num = notice_num

        return {G_NOTICE_NUM: g.notice_num}


def get_oauth2_config() -> dict:
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
            "reply_num": post["reply_num"],
            "view_num": post["view_num"],
            "like_num": post["like_num"],
            "save_num": post["save_num"],
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
            "view_num": popular["view_num"],
            "reply_num": popular["reply_num"],
        }
        for popular in populars
    ]


def get_home_stats() -> list:
    """Get index stats data."""

    stats_response = stats_service().json
    stats = stats_response.get("data").get("stats")

    return [
        [
            create_stat_label("Community", stats["community_num"]),
            create_stat_label("Request", stats["request_num"]),
        ],
        [
            create_stat_label("Reply", stats["reply_num"]),
            create_stat_label("View", stats["view_num"]),
        ],
        [
            create_stat_label("Like", stats["like_num"]),
            create_stat_label("Save", stats["save_num"]),
        ],
    ]


def create_stat_label(name: str, value: int) -> list:
    """Create stat labels."""

    return {"label": name, "value": value}


def get_home_communities() -> list:
    """Get index communities data."""

    communities_response = communities_service().json
    communities = communities_response.get("data").get("communities")

    return [
        {"id": community["id"], "name": community["name"]} for community in communities
    ]
