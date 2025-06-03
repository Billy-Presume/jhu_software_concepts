"""
Module: clean_test.py
Author: Billy Presume
Created: 2025-06-01
Modified: 2025-06-03
Description: Unit tests for clean.py module using pytest.
Note: Private functions (with leading underscore) are imported here **only for testing purposes**.
"""

from typing import Any
import pytest

from ..clean import clean_data, _parse_status_date, _parse_tags, save_data  # type: ignore


@pytest.mark.parametrize(
    "status_text, expected_date",
    [
        ("Accepted on 2025-05-01", "2025-05-01"),
        ("Rejected on 2024-12-31", "2024-12-31"),
        ("Waitlisted", None),
        ("", None),
        ("Accepted", None),
    ],
)
def test_parse_status_date(status_text: str, expected_date: Any) -> None:
    assert _parse_status_date(status_text) == expected_date


@pytest.mark.parametrize(
    "tags_list, expected",
    [
        (["Fall 2025", "GRE 320", "International"], {"fall 2025", "gre 320", "international"}),
        ([], set()),
        ([""], {""}),
        (["Accepted", "Waitlisted"], {"accepted", "waitlisted"}),
    ], # type: ignore
)
def test_parse_tags(tags_list: list[str], expected: set[str]) -> None:
    assert _parse_tags(tags_list) == expected


def test_clean_data_basic() -> None:
    raw_entries = [ # type: ignore
        {
            "university": "Uni A",
            "program_name": "Program X",
            "degree": "PhD",
            "date_added": "2025-01-01",
            "status": "Accepted on 2025-05-01",
            "url": "/link",
            "tags": ["Fall 2025", "GRE 320"],
            "comments": "Excited!",
        },
        {
            "university": "Uni B",
            "program_name": "",
            "degree": "",
            "date_added": "2024-12-12",
            "status": "Waitlisted",
            "url": "",
            "tags": [],
            "comments": "",
        },
    ]

    cleaned = clean_data(raw_entries) # type: ignore
    assert len(cleaned) == 2

    entry1 = cleaned[0]
    assert entry1["university"] == "Uni A"
    assert entry1["program_name"] == "Program X"
    assert entry1["degree"] == "PhD"
    assert entry1["date_added"] == "2025-01-01"
    assert entry1["status"] == "Accepted on 2025-05-01"
    assert entry1["status_date"] == "2025-05-01"
    assert entry1["url"] == "/link"

    # Make sure tags is a set and never None, so 'in' is valid
    assert isinstance(entry1["tags"], set)
    assert "fall 2025" in entry1["tags"]
    assert "gre 320" in entry1["tags"]

    assert entry1["comments"] == "Excited!"

    entry2 = cleaned[1]
    assert entry2["university"] == "Uni B"
    assert entry2["program_name"] == ""
    assert entry2["degree"] == ""
    assert entry2["status_date"] is None
    # tags is empty set, never None
    assert entry2["tags"] == set()
    assert entry2["comments"] == ""


def test_save_data_creates_file(tmp_path) -> None: # type: ignore
    data = [{ # type: ignore
        "university": "Test Uni",
        "program_name": "Test Prog",
        "degree": "MS",
        "date_added": "2025-01-01",
        "status": "Accepted",
        "url": "",
        "tags": set(),
        "comments": "",
    }]
    filename = tmp_path / "cleaned_data.json" # type: ignore
    result = save_data(data, base_filename=str(filename)) # type: ignore
    assert result is not None
    saved_file = tmp_path / result # type: ignore
    assert saved_file.exists() # type: ignore
    assert saved_file.read_text(encoding="utf-8") != "" # type: ignore


def test_save_data_no_data() -> None:
    result = save_data([], base_filename="should_not_exist.json") # type: ignore
    assert result is None
