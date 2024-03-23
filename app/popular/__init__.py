# pylint: skip-file

from flask import Blueprint

popular_bp = Blueprint(
    "popular",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/popular/static",
)

from . import routes
