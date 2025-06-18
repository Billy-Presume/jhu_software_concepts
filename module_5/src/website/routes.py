"""
Module: routes.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-17

Description:
    Defines route endpoints using Flask Blueprints, performs safe SQL query execution,
    and renders analytic results on the homepage.
"""

import logging
import os
from typing import Any

from flask import Blueprint, render_template
from psycopg import Connection

from src.website.query_data import execute_query
from src.utils.database import connect_to_database
from src.website.load_data import load_applicants

logger = logging.getLogger(__name__)
views = Blueprint("views", __name__)

DATA_FILE_2 = os.path.join(
    os.path.dirname(__file__), "static", "gradcafe_applicant_data", "applicant_data_2.json"
)


def load_if_first_time() -> None:
    """
    Loads applicant data from JSON files into the database if environment variable is set.

    Returns:
        None

    Side Effects:
        Modifies the `.env` file to disable subsequent loads.
    """
    if os.getenv("LOAD_DATA_ON_FIRST_RUN") == "1":
        try:
            logger.info("First run detected. Loading applicants into database...")
            connection: Connection = connect_to_database()  # type: ignore
            load_applicants(connection)
            load_applicants(connection, DATA_FILE_2)
            connection.close()

            env_path = ".env"
            if not os.path.exists(env_path):
                logger.error(".env file not found.")
                return

            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            with open(env_path, "w", encoding="utf-8") as f:
                updated = False
                for line in lines:
                    if line.startswith("export LOAD_DATA_ON_FIRST_RUN=1"):
                        f.write("export LOAD_DATA_ON_FIRST_RUN=0\n")
                        updated = True
                    else:
                        f.write(line)

                if not updated:
                    f.write("export LOAD_DATA_ON_FIRST_RUN=0\n")

            logger.info("Data loaded successfully. .env updated.")
        except Exception as e:
            logger.exception("Failed to load initial applicant data: %s", e)


def safe_fetch_query(query: str) -> list[tuple[Any, ...]]:
    """
    Executes a SQL query and returns results or an empty list on failure.

    Args:
        query (str): SQL query string (must be pre-validated or composed).

    Returns:
        list[tuple[Any, ...]]: Query results or empty list if failed.
    """
    try:
        connection = connect_to_database()
        results = execute_query(connection, query)
        if connection and not connection.closed:
            connection.close()
        return results or []
    except Exception as e:
        logger.error("Query failed: %s\nError: %s", query, e)
        return []


@views.route("/")
@views.route("/home")
def home():
    """
    Renders the homepage with analytics derived from the applicants database.

    Returns:
        HTML template: Rendered home page with tabulated data.
    """
    questions: list[tuple[str, list[str], list[Any]]] = []

    # 1. Count of entries for Fall 2025 (LIMIT 1 since COUNT returns one row)
    query1 = "SELECT COUNT(*) FROM applicants WHERE term = 'Fall 2025' LIMIT 1"
    fall_2025_count = safe_fetch_query(query1)[0][0]

    questions.append(
        ("How many entries applied for Fall 2025?", ["Total Entries"], [fall_2025_count])
    )

    # 2. International applicant count and total count (LIMIT 1 each)
    query2_intl = "SELECT COUNT(*) FROM applicants WHERE us_or_international NOT IN ('American', 'Other') LIMIT 1"
    intl = safe_fetch_query(query2_intl)[0][0]

    query2_total = "SELECT COUNT(*) FROM applicants LIMIT 1"
    total = safe_fetch_query(query2_total)[0][0]

    intl_percent = round((intl / total) * 100, 2) if total else 0
    questions.append((
        "What percentage of entries are international?", ["International %"], [f"{intl_percent}%"]
    ))

    # 3. Average GPA, GRE, GRE V, GRE AW for all applicants providing those values (LIMIT 1)
    query3 = (
        "SELECT "
        "ROUND(AVG(gpa)::NUMERIC, 2), "
        "ROUND(AVG(gre)::NUMERIC, 1), "
        "ROUND(AVG(gre_v)::NUMERIC, 1), "
        "ROUND(AVG(gre_aw)::NUMERIC, 2) "
        "FROM applicants "
        "WHERE gpa IS NOT NULL OR gre IS NOT NULL OR gre_v IS NOT NULL OR gre_aw IS NOT NULL "
        "LIMIT 1"
    )
    q3_result = safe_fetch_query(query3)[0]
    questions.append((
        "Average GPA, GRE, GRE V, GRE AW for all applicants providing those values?",
        ["Avg. GPA", "Avg. GRE", "Avg. GRE V", "Avg. GRE AW"], list(q3_result)
    ))

    # 4. Average GPA of American students in Fall 2025 (LIMIT 1)
    query4 = (
        "SELECT ROUND(AVG(gpa)::NUMERIC, 2) FROM applicants "
        "WHERE us_or_international = 'American' AND term = 'Fall 2025' AND gpa IS NOT NULL "
        "LIMIT 1"
    )
    avg_gpa_american = safe_fetch_query(query4)[0][0]
    questions.append((
        "Average GPA of American students applying for Fall 2025?", ["Avg. American GPA"],
        [avg_gpa_american]
    ))

    # 5. Acceptance rate for Fall 2025 (LIMIT 1)
    query5 = (
        "SELECT COUNT(*) FROM applicants "
        "WHERE status ILIKE 'Accepted' AND term = 'Fall 2025' "
        "LIMIT 1"
    )
    accepted_count = safe_fetch_query(query5)[0][0]

    acceptance_percent = round((accepted_count / fall_2025_count) *
                               100, 2) if fall_2025_count else 0
    questions.append(
        ("Acceptance percentage for Fall 2025?", ["Acceptance %"], [f"{acceptance_percent}%"])
    )

    # 6. GPA of accepted Fall 2025 applicants (LIMIT 1)
    query6 = (
        "SELECT ROUND(AVG(gpa)::NUMERIC, 2) FROM applicants "
        "WHERE term = 'Fall 2025' AND status ILIKE 'Accepted' AND gpa IS NOT NULL "
        "LIMIT 1"
    )
    accepted_gpa = safe_fetch_query(query6)[0][0]
    questions.append(
        ("Average GPA for accepted applicants in Fall 2025?", ["Avg. GPA"], [accepted_gpa])
    )

    # 7. JHU CS Masters applicants (LIMIT 1)
    query7 = (
        "SELECT COUNT(*) FROM applicants "
        "WHERE university ILIKE '%JHU%' "
        "AND program ILIKE '%Computer Science%' "
        "AND degree ILIKE '%Master%' "
        "LIMIT 1"
    )
    jhu_cs_count = safe_fetch_query(query7)[0][0]
    questions.append((
        "How many applicants applied to JHU for a CS Master's?", ["JHU CS Masters Applicants"],
        [jhu_cs_count]
    ))

    context: dict[str, list[tuple[Any, ...]] |
                  list[tuple[str, list[str], list[Any]]]] = {"questions": questions}

    return render_template("index.html", zip=zip, **context)
