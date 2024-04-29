"""Extensions module, singletons for the application."""

from flasgger import Swagger
from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .constants import FlashAlertTypeEnum

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.auth"
login_manager.login_message = "Please log in."
login_manager.login_message_category = FlashAlertTypeEnum.PRIMARY.value
bcrypt = Bcrypt()
scheduler = APScheduler()
jwt = JWTManager()
swag = Swagger()
