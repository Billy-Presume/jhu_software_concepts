"""
Module: database.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-04
Description: Provides database connection and query execution.
"""

import os
import psycopg2
from psycopg2 import extensions
from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()


def connect_to_database() -> extensions.connection:
    """
    Connects to the PostgreSQL database.

    Returns:
        connection: psycopg2 database connection.
    """
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432"))
    )
