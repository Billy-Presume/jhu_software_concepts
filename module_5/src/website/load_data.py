"""
Module: load_data.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-17

Description:
    Loads data from a JSON file into the PostgreSQL 'applicants' table securely using psycopg3.
"""

import os
import json
import logging
from datetime import datetime
from typing import TypedDict, Optional, cast

from psycopg import Connection
from psycopg.sql import SQL, Identifier, Placeholder

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DATA_FILE = os.path.join(
    os.path.dirname(__file__), 'static', 'gradcafe_applicant_data', 'applicant_data.json'
)


class ApplicantRecord(TypedDict, total=False):
    """Represents the expected structure of each JSON record."""
    university: Optional[str]
    program_name: Optional[str]
    date_added: Optional[str]
    term: Optional[str]
    status: Optional[str]
    decision_date: Optional[str]
    comments: Optional[str]
    us_international: Optional[str]
    gre_score: Optional[str]
    gre_v_score: Optional[str]
    gre_aw_score: Optional[str]
    degree: Optional[str]
    gpa: Optional[str]
    url: Optional[str]
    gre: Optional[str]
    gre_v: Optional[str]
    gre_aw: Optional[str]
    us_or_international: Optional[str]


def load_json_data(file_path: str) -> list[ApplicantRecord]:
    """Load and validate JSON data from a file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list[ApplicantRecord]: List of valid applicant records.

    Raises:
        FileNotFoundError: If file not found.
        json.JSONDecodeError: If JSON is malformed.
        ValueError: If top-level object is not a list.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected top-level JSON to be a list.")

    data = cast(list[ApplicantRecord], data)
    logger.info("Loaded %d records from JSON.", len(data))
    return data


def parse_float(value: Optional[str]) -> Optional[float]:
    """Parse float safely from string.

    Args:
        value (Optional[str]): Input string.

    Returns:
        Optional[float]: Parsed float or None.
    """
    try:
        return float(value) if value is not None else None
    except ValueError:
        return None


def parse_date(value: Optional[str]) -> Optional[str]:
    """Parse and format a date string into ISO format.

    Args:
        value (Optional[str]): Input date string.

    Returns:
        Optional[str]: ISO-formatted date or None.
    """
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat() if value else None
    except ValueError:
        return None


def create_applicants_table(connection: Connection) -> None:
    """Create the applicants table if it does not already exist.

    Args:
        connection (Connection): psycopg3 database connection.
    """
    query = SQL(
        """
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
        )
    """
    )

    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
        logger.info("Created or verified 'applicants' table.")


def insert_applicant(connection: Connection, record: ApplicantRecord) -> None:
    """Insert a single applicant into the applicants table.

    Args:
        connection (Connection): psycopg3 database connection.
        record (ApplicantRecord): One parsed applicant entry.
    """
    query = SQL(
        """
        INSERT INTO {table} (
            university, program, date_added, term, status, decision_date,
            comments, us_or_international, gpa, gre, gre_v, gre_aw, degree, url
        ) VALUES (
            {university}, {program}, {date_added}, {term}, {status}, {decision_date},
            {comments}, {us_or_international}, {gpa}, {gre}, {gre_v}, {gre_aw}, {degree}, {url}
        )
    """
    ).format(
        table=Identifier("applicants"),
        university=Placeholder("university"),
        program=Placeholder("program"),
        date_added=Placeholder("date_added"),
        term=Placeholder("term"),
        status=Placeholder("status"),
        decision_date=Placeholder("decision_date"),
        comments=Placeholder("comments"),
        us_or_international=Placeholder("us_or_international"),
        gpa=Placeholder("gpa"),
        gre=Placeholder("gre"),
        gre_v=Placeholder("gre_v"),
        gre_aw=Placeholder("gre_aw"),
        degree=Placeholder("degree"),
        url=Placeholder("url")
    )

    values: dict[str, str | float | None] = {
        "university": record.get("university"),
        "program": record.get("program_name"),
        "date_added": parse_date(record.get("date_added")),
        "term": record.get("term"),
        "status": record.get("status"),
        "decision_date": parse_date(record.get("decision_date")),
        "comments": record.get("comments"),
        "us_or_international": record.get("us_international") or record.get("us_or_international"),
        "gpa": parse_float(record.get("gpa")),
        "gre": parse_float(record.get("gre_score")) or parse_float(record.get("gre")),
        "gre_v": parse_float(record.get("gre_v_score")) or parse_float(record.get("gre_v")),
        "gre_aw": parse_float(record.get("gre_aw_score")) or parse_float(record.get("gre_aw")),
        "degree": record.get("degree"),
        "url": record.get("url"),
    }

    with connection.cursor() as cursor:
        cursor.execute(query, values)


def load_applicants(connection: Connection, json_path: str = DATA_FILE) -> None:
    """Load all applicants from the JSON file into the database.

    Args:
        connection (Connection): psycopg3 database connection.
        json_path (str): Path to the JSON file.
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
        logger.info("Inserted %d records into 'applicants' table.", len(applicants))

    except Exception as err:
        logger.exception("Failed to load applicants: %s", err)
        connection.rollback()
        logger.error("Transaction rolled back due to error.")
