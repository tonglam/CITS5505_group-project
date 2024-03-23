# pylint: skip-file

from flask import Blueprint

post_bp = Blueprint(
    "post",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/post/static",
)

from . import routes
