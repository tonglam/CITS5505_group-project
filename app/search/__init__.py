# pylint: skip-file

from flask import Blueprint

search_bp = Blueprint(
    "search",
    __name__,
    template_folder="templates",
    static_folder="static",
)

from . import routes
