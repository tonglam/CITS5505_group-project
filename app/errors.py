""" error handling """

from flask import render_template

from app.constants import HttpRequstEnum

from .extensions import db


def register_error_handlers(app):
    """Registers error handlers for common HTTP error codes."""

    @app.errorhandler(HttpRequstEnum.BAD_REQUEST.value)
    def bad_request_error(_):
        return render_template("errors/400.html"), HttpRequstEnum.BAD_REQUEST.value

    @app.errorhandler(HttpRequstEnum.UNAUTHORIZED.value)
    def unauthorized_error(_):
        return render_template("errors/401.html"), HttpRequstEnum.UNAUTHORIZED.value

    @app.errorhandler(HttpRequstEnum.FORBIDDEN.value)
    def forbidden_error(_):
        return render_template("errors/403.html"), HttpRequstEnum.FORBIDDEN.value

    @app.errorhandler(HttpRequstEnum.NOT_FOUND.value)
    def page_not_found_error(_):
        return render_template("errors/404.html"), HttpRequstEnum.NOT_FOUND.value

    @app.errorhandler(HttpRequstEnum.METHOD_NOT_ALLOWED.value)
    def method_not_allowed_error(_):
        return (
            render_template("errors/405.html"),
            HttpRequstEnum.METHOD_NOT_ALLOWED.value,
        )

    @app.errorhandler(HttpRequstEnum.INTERNAL_SERVER_ERROR.value)
    def internal_server_error(_):
        db.session.rollback()
        return (
            render_template("errors/500.html"),
            HttpRequstEnum.INTERNAL_SERVER_ERROR.value,
        )
