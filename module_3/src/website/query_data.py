"""
Module: query_data.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-04
Description: This module provides a function `execute_query` that allows database interaction functions using psycopg2.
"""

import logging
from typing import Any

from psycopg2 import extensions, OperationalError, ProgrammingError, IntegrityError, DatabaseError

logger = logging.getLogger(__name__)


def execute_query(
    connection: extensions.connection | None,
    query: str,
    params: tuple[Any, ...] | list[Any] | None = None
) -> list[tuple[Any, ...]] | None:
    """Safely executes a sanitized SQL query.

    Args:
        connection: psycopg2 database connection or None.
        query: Sanitized SQL query string.
        params: Optional parameters for the query.

    Returns:
        List of rows for SELECT queries, or None for others.
    """
    if connection is None or connection.closed != 0:
        raise ValueError('Database connection is not open.')

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)

        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            logger.info('Query returned %d row(s).', len(results))
            return results
        else:
            connection.commit()
            logger.info('Non-SELECT query committed successfully.')
            return None

    except OperationalError as e:
        connection.rollback()
        logger.error('OperationalError: %s', e)
    except ProgrammingError as e:
        connection.rollback()
        logger.error('ProgrammingError: %s', e)
    except IntegrityError as e:
        connection.rollback()
        logger.error('IntegrityError: %s', e)
    except DatabaseError as e:
        connection.rollback()
        logger.error('DatabaseError: %s', e)
    except Exception as e:
        connection.rollback()
        logger.exception('Unexpected error during query execution: %s', e)
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception as close_err:
                logger.warning('Failed to close cursor: %s', close_err)

    return None