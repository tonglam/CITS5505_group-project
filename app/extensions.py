"""Extensions module, singletons for the application."""

from flasgger import Swagger
from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from .constants import FlashAlertTypeEnum


def get_db_meta_data() -> MetaData:
    """Get the database metadata."""

    naming_convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    return MetaData(naming_convention=naming_convention)


# flask-sqlalchemy
meta_data = get_db_meta_data()
db = SQLAlchemy(metadata=meta_data)

# flask-login
login_manager = LoginManager()
login_manager.login_view = "auth.auth"
login_manager.login_message = "Please log in."
login_manager.login_message_category = FlashAlertTypeEnum.PRIMARY.value

# flask-bcrypt
bcrypt = Bcrypt()

# flask-apscheduler
scheduler = APScheduler()

# flask-jwt-extended
jwt = JWTManager()

# flasgger
swag = Swagger()
