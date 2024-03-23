# pylint: skip-file

from flask import Blueprint

notice_bp = Blueprint(
    "notice",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/notice/static",
)

from . import routes
