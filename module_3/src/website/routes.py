"""
Module: routes.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-05
Description: Defines route endpoints using Flask Blueprints.
"""

import logging
import os
from typing import Any
from flask import Blueprint, render_template

from .query_data import execute_query
from ..utils.database import connect_to_database
from .load_data import load_applicants

logger = logging.getLogger(__name__)
views = Blueprint("views", __name__)

# Path to the secondary data file
DATA_FILE_2 = os.path.join(
    os.path.dirname(__file__), 'static', 'gradcafe_applicant_data', 'applicant_data_2.json'
)


def load_if_first_time() -> None:
    """
    Loads applicant data from JSON into the database on first run,
    and updates the .env file to prevent future runs.
    """

    if os.getenv("LOAD_DATA_ON_FIRST_RUN") == "1":
        try:
            logger.info("First run detected. Loading applicants into database...")
            connection = connect_to_database()
            load_applicants(connection)
            load_applicants(connection, DATA_FILE_2)
            connection.close()

            env_path = ".env"
            if not os.path.exists(env_path):
                logger.error(".env file not found.")
                return

            # Update .env to disable future loads
            with open(env_path, "r") as f:
                lines = f.readlines()

            with open(env_path, "w") as f:
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
        query (str): SQL query to execute.

    Returns:
        list[tuple[Any, ...]]: Query results or empty list on error.
    """
    try:
        connection = connect_to_database()
        results = execute_query(connection, query)

        if connection and not connection.closed:
            connection.close()

        return results or []

    except Exception as e:
        logger.error("Failed to fetch data for query: %s\nError: %s", query, e)
        return []


@views.route("/")
@views.route("/home")
def home():
    """
    Renders the homepage with structured applicant data displayed as questions and answers.
    """

    # Loads the data from json to postgres database if is first run
    # load_if_first_time()

    questions: list[tuple[str, list[str], list[Any]]] = []

    # 1. Count of entries for Fall 2025
    result = safe_fetch_query("SELECT COUNT(*) FROM applicants WHERE term = 'Fall 2025'")
    fall_2025_count = result[0][0] if result and result[0] else 0
    questions.append((
        "How many entries do you have in your database who have applied for Fall 2025?",
        ["Total Entries"], [fall_2025_count]
    ))

    # 2. Percentage of international students (not American or Other)
    intl_result = safe_fetch_query(
        """
        SELECT COUNT(*) FROM applicants 
        WHERE us_or_international NOT IN ('American', 'Other')
    """
    )
    total_result = safe_fetch_query("SELECT COUNT(*) FROM applicants")
    intl_count = intl_result[0][0] if intl_result and intl_result[0] else 0
    total_count = total_result[0][0] if total_result and total_result[0] else 0
    intl_percent = round((intl_count / total_count) * 100, 2) if total_count else 0
    questions.append((
        "What percentage of entries are from international students (not American or Other)?",
        ["International %"], [f"{intl_percent}%"]
    ))

    # 3. Average GPA, GRE, GRE V, GRE AW
    q3_result = safe_fetch_query(
        """
        SELECT 
            ROUND(AVG(gpa)::NUMERIC, 2), 
            ROUND(AVG(gre)::NUMERIC, 1), 
            ROUND(AVG(gre_v)::NUMERIC, 1), 
            ROUND(AVG(gre_aw)::NUMERIC, 2)
        FROM applicants
        WHERE gpa IS NOT NULL OR gre IS NOT NULL OR gre_v IS NOT NULL OR gre_aw IS NOT NULL
    """
    )
    q3_values = list(q3_result[0]) if q3_result and q3_result[0] else [None, None, None, None]
    questions.append((
        "What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?",
        ["Avg. GPA", "Avg. GRE", "Avg. GRE V", "Avg. GRE AW"], q3_values
    ))

    # 4. Average GPA of American students in Fall 2025
    q4_result = safe_fetch_query(
        """
        SELECT ROUND(AVG(gpa)::NUMERIC, 2) FROM applicants 
        WHERE us_or_international = 'American' AND term = 'Fall 2025' AND gpa IS NOT NULL
    """
    )
    avg_gpa_american = q4_result[0][0] if q4_result and q4_result[0] else None
    questions.append((
        "What is the average GPA of American students in Fall 2025?", ["Avg. American GPA"],
        [avg_gpa_american]
    ))

    # 5. Percent of Fall 2025 entries that are Acceptances
    accepted_result = safe_fetch_query(
        """
        SELECT COUNT(*) FROM applicants 
        WHERE status ILIKE 'Accepted' AND term = 'Fall 2025'
    """
    )
    accepted_count = accepted_result[0][0] if accepted_result and accepted_result[0] else 0
    acceptance_percent = round((accepted_count / fall_2025_count) *
                               100, 2) if fall_2025_count else 0
    questions.append((
        "What percent of entries for Fall 2025 are Acceptances?", ["Acceptance %"],
        [f"{acceptance_percent}%"]
    ))

    # 6. Average GPA of accepted applicants for Fall 2025
    q6_result = safe_fetch_query(
        """
        SELECT ROUND(AVG(gpa)::NUMERIC, 2) FROM applicants 
        WHERE term = 'Fall 2025' AND status ILIKE 'Accepted' AND gpa IS NOT NULL
    """
    )
    accepted_gpa = q6_result[0][0] if q6_result and q6_result[0] else None
    questions.append((
        "What is the average GPA of applicants who applied for Fall 2025 and were accepted?",
        ["Avg. GPA"], [accepted_gpa]
    ))

    # 7. JHU CS Master's applicants
    q7_result = safe_fetch_query(
        """
        SELECT COUNT(*) FROM applicants 
        WHERE university ILIKE '%JHU%' 
          AND program ILIKE '%Computer Science%' 
          AND degree ILIKE '%Master%'
    """
    )
    jhu_cs_count = q7_result[0][0] if q7_result and q7_result[0] else 0
    questions.append((
        "How many entries are from applicants who applied to JHU for a master's in Computer Science?",
        ["JHU CS Masters Applicants"], [jhu_cs_count]
    ))

    # Render the template with context
    context: dict[str, list[tuple[Any, ...]] |
                  list[tuple[str, list[str], list[Any]]]] = {"questions": questions}

    return render_template("index.html", zip=zip, **context)
