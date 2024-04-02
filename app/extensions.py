"""Extensions module, singletons for the application."""

from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.constant import FlashAlertTypeEnum

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in."
login_manager.login_message_category = FlashAlertTypeEnum.PRIMARY.value
bcrypt = Bcrypt()
scheduler = APScheduler()
