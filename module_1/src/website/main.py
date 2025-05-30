"""
Module: app.py
Author: Billy Presume
Created: 2025-05-29
Modified: 2025-05-30
Description: Entry point for running the Flask application.
"""

import socket
from flask import Flask
from . import create_app

def find_free_port(default: int = 8000, max_tries: int = 100) -> int:
    """
    Find an available TCP port starting from the given default.

    Args:
        default (int): The starting port number to check from. Defaults to 8000.
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
    # The below line might cause a W0621: (redefined-outer-name) linting warning but I prefer calling the find_free_port function and pass the available port to the app
    port: int = find_free_port()
    print(f"Running on http://0.0.0.0:{port}")
    app.run(
        debug=True,
        host="0.0.0.0",  # All available interfaces
        port=port  # Dynamically chosen free port
    )
