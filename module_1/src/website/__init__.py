"""
Module: __init__.py
Author: Billy Presume
Created: 2025-05-29
Modified: 2025-06-1
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
    app.secret_key = '13SBYPF1KeRZE3D8rKSqviBuVnrn1Jql7/+Q0D/bCa5zxA4h8lOtcOV37wvJ1V3t'  # Will be moved to .env
    return app
