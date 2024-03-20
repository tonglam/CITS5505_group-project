"""Extensions module, singletons for the application."""

from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.auth"
login_manager.login_message = "Please log in."
login_manager.login_message_category = "info"
bcrypt = Bcrypt()
scheduler = APScheduler()
