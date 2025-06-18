"""
Module: query_data.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-17
Description: Secure query execution using psycopg3 with full type safety and logging.
"""

import logging
from typing import Any, Sequence

from psycopg import Connection
from psycopg.errors import OperationalError, ProgrammingError, IntegrityError, DatabaseError
from psycopg.sql import SQL, Composed

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute_query(
    connection: Connection | None,
    query: str | SQL | Composed,
    params: Sequence[Any] | None = None
) -> list[tuple[Any, ...]] | None:
    """
    Executes a parameterized or composed SQL query using psycopg3.

    Args:
        connection (Connection | None): A valid psycopg3 connection.
        query (str | SQL | Composed): SQL query (raw or composed).
        params (Sequence[Any] | None): Query parameters.

    Returns:
        list[tuple[Any, ...]] | None: Rows for SELECT queries, else None.

    Raises:
        ValueError: If connection is invalid.
    """
    if connection is None or connection.closed:
        raise ValueError("Database connection is not open.")

    try:
        with connection.cursor() as cursor:
            cursor.execute(SQL(query), params)  # type: ignore

            if str(query).strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                logger.info("Query returned %d row(s).", len(results))
                return results

            connection.commit()
            logger.info("Non-SELECT query executed successfully.")
            return None

    except (OperationalError, ProgrammingError, IntegrityError, DatabaseError) as err:
        connection.rollback()
        logger.error("Database error occurred: %s", err)
    except Exception as err:
        connection.rollback()
        logger.exception("Unexpected error: %s", err)

    return None
