"""
Module: load_data.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-04
Description: Loads data from a JSON file into the PostgreSQL 'applicants' table.
"""

import os
import json
import logging
from datetime import datetime
from typing import TypedDict

from psycopg2 import extensions

logger = logging.getLogger(__name__)

# Use absolute path based on the script's directory
DATA_FILE = os.path.join(
    os.path.dirname(__file__), 'static', 'gradcafe_applicant_data', 'applicant_data.json'
)


class ApplicantRecord(TypedDict, total=False):
    """TypedDict representing the expected structure of each JSON record."""
    university: str | None
    program_name: str | None
    date_added: str | None
    term: str | None
    status: str | None
    decision_date: str | None
    comments: str | None
    us_international: str | None
    gre_score: str | None
    gre_v_score: str | None
    gre_aw_score: str | None
    degree: str | None
    gpa: str | None
    url: str | None


def load_json_data(file_path: str) -> list[ApplicantRecord]:
    """Loads and parses a JSON file into a list of ApplicantRecord dicts.

    Args:
        file_path: Path to the JSON file to load.

    Returns:
        A list of dictionaries, each representing an applicant record.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file does not contain a list.
        json.JSONDecodeError: If the JSON is invalid.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File not found: {file_path}')

    with open(file_path, encoding='utf-8') as f:
        data: list[ApplicantRecord] = json.load(f)

    if not isinstance(data, list):  # type: ignore
        raise ValueError('JSON data must be a list of objects.')

    logger.info('Loaded %d records from JSON.', len(data))
    return data


def create_applicants_table(connection: extensions.connection) -> None:
    """Creates the `applicants` table if it does not already exist.

    Args:
        connection: A valid PostgreSQL connection object.
    """
    query = """
    CREATE TABLE IF NOT EXISTS applicants (
        p_id SERIAL PRIMARY KEY,
        university TEXT,
        program TEXT,
        date_added DATE,
        term TEXT,
        status TEXT,
        decision_date DATE,
        comments TEXT,
        us_or_international TEXT,
        gpa FLOAT,
        gre FLOAT,
        gre_v FLOAT,
        gre_aw FLOAT,
        degree TEXT,
        url TEXT
    );
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
        logger.info("Ensured 'applicants' table exists.")


def parse_float(value: str | None) -> float | None:
    """Safely parses a string to a float.

    Args:
        value: String or None representing a numeric value.

    Returns:
        Parsed float value, or None if conversion fails or value is None.
    """
    try:
        return float(value) if value is not None else None
    except ValueError:
        return None


def parse_date(value: str | None) -> str | None:
    """Parses a string into an ISO-formatted date.

    Args:
        value: A date string in 'YYYY-MM-DD' format or None.

    Returns:
        A date string in ISO format, or None if parsing fails.
    """
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError:
        return None


def insert_applicant(connection: extensions.connection, record: ApplicantRecord) -> None:
    """Inserts a single applicant record into the database.

    Args:
        connection: A valid PostgreSQL connection object.
        record: Dictionary representing one applicant's data.

    Raises:
        psycopg2.DatabaseError: On any database error.
    """
    query = """
    INSERT INTO applicants (
        university, program, date_added, term, status, decision_date,
        comments, us_or_international, gpa, gre, gre_v, gre_aw, degree, url
    ) VALUES (
        %(university)s, %(program)s, %(date_added)s, %(term)s, %(status)s,
        %(decision_date)s, %(comments)s, %(us_or_international)s, %(gpa)s,
        %(gre)s, %(gre_v)s, %(gre_aw)s, %(degree)s, %(url)s
    );
    """

    values: dict[str, str | float | None] = {
        'university': record.get('university'), 'program': record.get('program_name'),
        'date_added': parse_date(record.get('date_added')), 'term': record.get('term'), 'status':
            record.get('status'), 'decision_date': parse_date(record.get('decision_date')
                                                             ), 'comments': record.get('comments'),
        'us_or_international': record.get('us_international') or record.get('us_or_international'),
        'gpa': parse_float(record.get('gpa')),
        'gre': parse_float(record.get('gre_score')) or parse_float(record.get('gre')),
        'gre_v': parse_float(record.get('gre_v_score')) or parse_float(record.get('gre_v')),
        'gre_aw': parse_float(record.get('gre_aw_score')) or parse_float(record.get('gre_aw')),
        'degree': record.get('degree'), 'url': record.get('url')
    }

    with connection.cursor() as cursor:
        cursor.execute(query, values)


def load_applicants(connection: extensions.connection, json_path: str = DATA_FILE) -> None:
    """Main entry point to load and insert applicant data from JSON into the database.

    Args:
        connection: A valid PostgreSQL connection object.
        json_path: Optional path to the JSON file (defaults to `applicants_data.json`).
    """
    try:
        create_applicants_table(connection)
        applicants = load_json_data(json_path)

        for idx, record in enumerate(applicants, start=1):
            try:
                insert_applicant(connection, record)
            except Exception as err:
                logger.error("Failed to insert record #%d: %s", idx, err)

        connection.commit()
        logger.info('All valid records have been inserted.')

    except Exception as err:
        logger.exception('Failed to load applicants: %s', err)
        connection.rollback()
