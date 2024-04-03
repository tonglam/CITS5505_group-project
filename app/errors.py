""" error handling """

from flask import render_template
from .extensions import db

def register_error_handlers(app):
    """Registers error handlers for common HTTP error codes."""
    @app.errorhandler(400)
    def bad_request_error(_):
        return render_template('errors/400.html'), 400

    @app.errorhandler(401)
    def unauthorized_error(_):
        return render_template('errors/401.html'), 401

    @app.errorhandler(404)
    def page_not_found_error(_):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(_):
        db.session.rollback()
        return render_template('errors/500.html'), 500
