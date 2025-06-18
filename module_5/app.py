"""
Module: app.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-17
Description: Entry point for running the Flask application.
"""

# Flask (3.1.1) is the core web framework used to build your application,
# relying on Werkzeug (3.1.3) for routing and request handling,
# Jinja2 (3.1.6) for templating,
# itsdangerous (2.2.0) for securely signing data,
# and MarkupSafe (3.0.2) for safely rendering text in templates.

# Click (8.2.1) is used by Flask to create command-line interfaces,
# simplifying app management commands.

# Blinker (1.9.0) provides support for signals in Flask,
# enabling event-driven programming.

# python-dotenv (1.1.0) helps load environment variables from a .env file,
# facilitating configuration without hardcoding secrets.

# psycopg[binary]>=3.2.9 is a PostgreSQL database adapter,
# likely used for database connections.

# For development and testing:
# - pytest (8.3.5) is used for running tests,
# - yapf (0.43.0) for code formatting,
# - pylint (3.3.7) for code linting to ensure code quality.

# pydeps (>=3.0.1) and graphviz (>=0.21) are used to analyze and visualize code dependencies,
# helpful in understanding module relationships within the project.


import socket
from flask import Flask

from src.website import create_app


def find_free_port(default: int = 5000, max_tries: int = 100) -> int:
    """
    Find an available TCP port starting from the given default.

    Args:
        default (int): The starting port number to check from. Defaults to 5000.
        max_tries (int): The maximum number of ports to try. Defaults to 100.

    Returns:
        int: An available port number.

    Raises:
        RuntimeError: If no available port is found within the range.
    """

    for port in range(default, default + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free port found.")


app: Flask = create_app()

if __name__ == "__main__":
    port: int = find_free_port()
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=port)
