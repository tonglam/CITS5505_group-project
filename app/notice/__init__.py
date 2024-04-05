# pylint: skip-file

from flask import Blueprint

notice_bp = Blueprint(
    "notice",
    __name__,
    template_folder="templates",
    static_folder="static",
)

from . import routes
