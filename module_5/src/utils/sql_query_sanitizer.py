"""
Module: sql_query_sanitizer.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-17

Description:
    Provides a function `sanitize_sql_query` to validate PostgreSQL SQL queries
    for basic safety and structure before execution.

Note:
    This is not a substitute for parameterized queries. All inputs should be
    composed using `psycopg.sql` utilities. This is meant for setup validation
    and internal use only — not direct user input.
"""

import re


def sanitize_sql_query(query: str) -> str:
    """Sanitizes a SQL query string to prevent unsafe patterns.

    This validator performs lightweight static analysis on the query string to:
    - Block multiple statements (stacking)
    - Reject dangerous patterns (UNION, DROP, SLEEP, etc.)
    - Enforce safe starting clauses (SELECT, INSERT, UPDATE, DELETE)
    - Remove inline and block comments
    - Check quote balancing and suspicious literals

    Args:
        query (str): Raw SQL query string.

    Returns:
        str: Cleaned and validated SQL string.

    Raises:
        ValueError: If the query is unsafe or malformed.
    """
    if not isinstance(query, str):  # type: ignore
        raise ValueError("Query must be a string.")

    query = query.strip()
    query = re.sub(r"\s+", " ", query)

    if len(query) < 5:
        raise ValueError("Query too short to be valid.")

    # Strip comments
    query = re.sub(r"--.*?$", "", query, flags=re.MULTILINE)
    query = re.sub(r"/\*.*?\*/", "", query, flags=re.DOTALL)

    # Uppercase for pattern matching
    upper_query = query.upper()

    # Reject stacked queries
    if ";" in query:
        raise ValueError("Semicolons are not allowed (no stacked queries).")

    # Known dangerous patterns
    forbidden_patterns = [
        r"UNION\s+SELECT",
        r"DROP\s+TABLE",
        r"TRUNCATE\s+TABLE",
        r"INSERT\s+INTO\s+\w+\s+SELECT",
        r"SLEEP\s*\(",
        r"WAITFOR\s+DELAY",
        r"\bOR\b\s+1=1",
        r"\bAND\b\s+1=1",
        r"\bOR\b\s+\d+=\d+",
        r"\bEXEC\b",
        r"\bXP_",  # XP_ is for extended procedures in SQL Server
        r"CHR\(",
        r"CAST\(",
        r"#",  # MySQL-style comment
        r"/\*",  # Start of block comment
    ]

    for pattern in forbidden_patterns:
        if re.search(pattern, upper_query):
            raise ValueError(f"Query rejected due to dangerous pattern: {pattern}")

    allowed_prefixes = ("SELECT ", "UPDATE ", "DELETE ", "INSERT INTO ")
    if not upper_query.startswith(allowed_prefixes):
        raise ValueError("Only SELECT, INSERT, UPDATE, and DELETE queries are allowed.")

    # Disallow binary or hex literals
    if re.search(r"(0x[0-9A-Fa-f]+|b'[01]+')", query):
        raise ValueError("Binary or hex literals are not allowed.")

    # Quote balancing
    if query.count("'") % 2 != 0 or query.count('"') % 2 != 0:
        raise ValueError("Unbalanced quotes in query.")

    # Enforce identifier length max
    for match in re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b", query):
        if len(match) > 64:
            raise ValueError(f"Identifier too long: {match}")

    return query
