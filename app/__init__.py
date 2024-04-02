"""Main application module."""

from flask import Flask, render_template
from flask_login import current_user, login_required

from app.api import api_bp
from app.auth import auth_bp
from app.community import community_bp
from app.extensions import bcrypt, db, login_manager, migrate, scheduler
from app.notice import notice_bp
from app.popular import popular_bp
from app.post import post_bp
from app.search import search_bp
from app.user import user_bp
from app.utils import get_config


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
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(notice_bp)
    app.register_blueprint(post_bp, url_prefix="/post")
    app.register_blueprint(popular_bp, url_prefix="/popular")
    app.register_blueprint(community_bp, url_prefix="/community")
    app.register_blueprint(user_bp, url_prefix="/user")

    @app.route("/")
    @app.route("/index")
    @login_required
    def index():
        return render_template("index.html")

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
            "authorize_url": get_config("GITHUB", "AUTHORIZE_URL"),
            "token_url": get_config("GITHUB", "TOKEN_URL"),
            "userinfo": {
                "url": get_config("GITHUB", "USER_URL"),
                "email": lambda json: json[0]["email"],
            },
            "scopes": ["user"],
        },
    }
