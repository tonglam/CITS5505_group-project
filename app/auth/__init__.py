# pylint: skip-file

from flask import Blueprint

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/auth/static",
)

from . import routes
