# pylint: skip-file

from flask import Blueprint

search_bp = Blueprint(
    "search",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/search/static",
)

from . import routes
