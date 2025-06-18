"""
Module: database.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-17

Description:
    Provides a secure PostgreSQL connection using psycopg v3.
"""

import os
import logging
from typing import Optional

from psycopg import connect, Connection
from psycopg.errors import OperationalError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def connect_to_database() -> Optional[Connection]:
    """
    Establishes a secure connection to a PostgreSQL database using environment variables.

    Returns:
        Optional[Connection]: psycopg database connection object or None on failure.

    Environment Variables Required:
        - DB_NAME: Database name
        - DB_USER: Username
        - DB_PASSWORD: Password
        - DB_HOST: Host (default: localhost)
        - DB_PORT: Port (default: 5432)
    """
    try:
        dbname = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")

        if not all([dbname, user, password]):
            raise EnvironmentError("Missing required database credentials in .env")

        conn = connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=int(port),
        )

        # logger.info("Successfully connected to the PostgreSQL database.")
        return conn

    except OperationalError as e:
        logger.error("Database connection failed: %s", e)
    except Exception as e:
        logger.exception("Unexpected error while connecting to the database: %s", e)

    return None
