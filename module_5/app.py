"""
Module: app.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-05
Description: Entry point for running the Flask application.
"""

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
