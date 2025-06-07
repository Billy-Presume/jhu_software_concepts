"""
Module: sql_query_sanitizer.py
Author: Billy Presume
Created: 2025-06-04
Modified: 2025-06-04
Description: This module provides a function `sanitize_sql_query` that attempts to clean and validate PostgreSQL SQL query strings to protect against common forms of SQL injection, CVE attacks, and other input-based exploits. 

Note: I am aware that this method is not foolproof and thatt parameterized query practices are best but this assignment will not be taking user input so this is just for setup completeness.
"""

import re


def sanitize_sql_query(query: str) -> str:
    """Sanitizes a SQL query string to prevent SQL injection and unsafe patterns.

    This function performs robust validation of a SQL query. It ensures that:
    - The query is a single safe SQL statement (no stacking with `;`)
    - Only `SELECT`, `INSERT`, `UPDATE`, or `DELETE` are allowed
    - Dangerous keywords, patterns, and comments are removed
    - No unbalanced quotes or suspicious literals are present

    Args:
        query: The raw SQL query string from user or untrusted source.

    Returns:
        A cleaned and validated SQL query string.

    Raises:
        ValueError: If the query is considered malformed or unsafe.
    """

    # 1. Ensure the input is a string and long enough to be meaningful.
    if not isinstance(query, str):  # type: ignore
        raise ValueError('Query must be a string.')

    query = query.strip()
    query = re.sub(r'\s+', ' ', query)  # Normalize all whitespace.

    if len(query) < 5:
        raise ValueError('Query too short to be valid.')

    # 2. Remove inline and block comments that can hide malicious code.
    query = re.sub(r'--.*?$', '', query, flags=re.MULTILINE)  # Single-line comments
    query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)  # Multi-line block comments

    upper_query = query.upper()

    # 3. Reject stacked queries using semicolons.
    if ';' in query:
        raise ValueError('Semicolons are not allowed (no stacked queries).')

    # 4. Block common SQL injection techniques and abuse patterns.
    forbidden_patterns = [
        r'UNION\s+SELECT',  # SQL injection data leak
        r'DROP\s+TABLE',  # Destructive queries
        r'TRUNCATE\s+TABLE',  # Silent destruction
        r'INSERT\s+INTO.*?SELECT',  # Data exfiltration
        r'SLEEP\s*\(',  # Time-based injection
        r'WAITFOR\s+DELAY',  # MSSQL time-based
        r'\bOR\b\s+1=1',  # Classic tautology
        r'\bAND\b\s+1=1',
        r'\bOR\b\s+\d+=\d+',
        r'\bEXEC\b',  # Remote command execution
        r'\bXP_\b',  # Remote command execution
        r'CHR\(',  # Bypasses and evasion
        r'CAST\(',  # Obfiscation
        r'#',  # Alternative comment
        r'/\*',  # Start of block comment
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, upper_query):
            raise ValueError(f'Query rejected due to dangerous pattern: {pattern}')

    # 5. Only allow a safe starting SQL verb.
    allowed_prefixes = (
        'SELECT ',
        'UPDATE ',
        'DELETE ',
        'INSERT INTO ',
    )
    if not upper_query.startswith(allowed_prefixes):
        raise ValueError('Only SELECT, INSERT, UPDATE, and DELETE queries are allowed.')

    # 6. Reject binary or hex literals that can be used for payloads.
    if re.search(r"(0x[0-9A-Fa-f]+|b'[01]+')", query):
        raise ValueError('Binary or hex literals are not allowed.')

    # 7. Ensure quotes are balanced to avoid injection through unclosed strings.
    if query.count("'") % 2 != 0 or query.count('"') % 2 != 0:
        raise ValueError('Unbalanced quotes in query.')

    # 8. Validate identifier lengths (table names, columns) to avoid obfuscation.
    identifier_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b')
    for match in identifier_pattern.findall(query):
        if len(match) > 64:
            raise ValueError(f'Identifier too long: {match}')

    return query
