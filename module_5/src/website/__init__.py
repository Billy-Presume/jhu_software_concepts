"""
Module: __init__.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-04
Description: Flask application factory and blueprint registration.
"""

from flask import Flask
from .routes import views


def create_app() -> Flask:
    """
    Flask application factory.

    Returns:
        Flask: A configured Flask application instance.
    """
    app = Flask(__name__)

    app.register_blueprint(views)
    return app
