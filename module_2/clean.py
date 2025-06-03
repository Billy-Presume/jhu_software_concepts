"""
Module: clean.py
Author: Billy Presume
Created: 2025-06-01
Modified: 2025-06-03
Description: Processes raw scraped GradCafe data and converts it into structured clean format,
             and supports loading/saving cleaned data with graceful error handling.
"""

import json
import logging
import re
from typing import Any, Optional

from scrape import scrape_multiple_pages

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def save_data(data: list[dict[str, Any]], filename: str = "applicant_data.json") -> bool:
    """Saves cleaned data to a JSON file.

    Args:
        data: Cleaned data list.
        filename: Output JSON filename.

    Returns:
        True if successful, False otherwise.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"Saved cleaned data to {filename}")
        return True
    except Exception as e:
        logging.error(f"Failed to save cleaned data to {filename}: {e}")
        return False


def clean_data(raw_data: list[dict[str, Any]]) -> list[dict[str, Optional[str]]]:
    """Cleans and structures the raw scraped data.

    Args:
        raw_data: Raw scraped entries.

    Returns:
        List of cleaned entries with standardized fields.
    """
    cleaned_results: list[dict[str, Optional[str]]] = []
    for entry in raw_data:
        acceptance_date, rejection_date = _parse_status_date(entry.get("status", ""))
        parsed_tags = _parse_tags(entry.get("tags", []))

        status_full = entry.get("status", "") or ""
        status_first_word = status_full.split()[0] if status_full else ""

        # Clean comments: remove HTML tags and decode escaped sequences into readable text
        raw_comments = entry.get("comments", "") or ""
        no_html = re.sub(r'<[^>]+>', '', raw_comments)  # remove html tags

        # Decode unicode escapes like \u2019 and surrogate pairs \ud83d\ude2c etc.
        # First encode raw string to bytes, then decode unicode-escape, then normalize whitespace
        try:
            decoded = no_html.encode('utf-8').decode('unicode_escape')
        except UnicodeDecodeError:
            decoded = no_html  # fallback if decoding fails

        # Normalize newlines and whitespace
        cleaned_comments = re.sub(r'[\r\n]+', ' ', decoded)  # replace newlines with space
        cleaned_comments = re.sub(r'\s+', ' ', cleaned_comments).strip()  # collapse spaces

        decision_date = acceptance_date if acceptance_date else rejection_date

        cleaned_results.append({
            "url": "https://www.thegradcafe.com" + (entry.get("url", "") or ""),
            "university": entry.get("university", "") or "",
            "program_name": entry.get("program_name", "") or "",
            "date_added": entry.get("date_added", "") or "",
            "term": parsed_tags.get("term", "") or "",
            "status": status_first_word,
            "decision_date": decision_date,
            "comments": cleaned_comments,
            "us_international": parsed_tags.get("us_international", "") or "",
            "gre_score": parsed_tags.get("gre_score", "") or "",
            "gre_v_score": parsed_tags.get("gre_v_score", "") or "",
            "gre_q_score": parsed_tags.get("gre_q_score", "") or "",
            "gre_aw_score": parsed_tags.get("gre_aw_score", "") or "",
            "degree": entry.get("degree", "") or "",
            "gpa": parsed_tags.get("gpa", "") or "",
        })

    logging.info(f"Cleaned {len(cleaned_results)} entries")
    return cleaned_results


def _parse_status_date(status: str) -> tuple[Optional[str], Optional[str]]:
    """Extract acceptance or rejection dates from status string.

    Args:
        status: Status string.

    Returns:
        Tuple of (acceptance_date, rejection_date).
    """
    acceptance_date: Optional[str] = None
    rejection_date: Optional[str] = None

    if not status:
        return acceptance_date, rejection_date

    lowered = status.lower()
    if "rejected on" in lowered:
        match = re.search(r"Rejected on (.+)", status, re.IGNORECASE)
        if match:
            rejection_date = match.group(1).strip()
    elif "accepted on" in lowered:
        match = re.search(r"Accepted on (.+)", status, re.IGNORECASE)
        if match:
            acceptance_date = match.group(1).strip()

    return acceptance_date, rejection_date


def _parse_tags(tags: list[str]) -> dict[str, Optional[str]]:
    """Parses tags list into structured info.

    Args:
        tags: List of tag strings.

    Returns:
        Dictionary with parsed fields.
    """
    info = {
        "term": "",
        "us_international": "",
        "gre_score": "",
        "gre_v_score": "",
        "gre_q_score": "",
        "gre_aw_score": "",
        "gpa": "",
    }

    for tag in tags:
        t = tag.lower()

        if re.fullmatch(r"(fall|spring|summer|winter) \d{4}", t):
            info["term"] = tag
        elif t in {"american", "us", "domestic", "us citizen"}:
            info["us_international"] = "American"
        elif t in {"international", "non-us", "intl", "int'l"}:
            info["us_international"] = "International"
        elif m := re.match(r"gre\s*(\d{2,3})", t):
            info["gre_score"] = m.group(1)
        elif m := re.match(r"gre v[: ]\s*(\d{2,3})", t):
            info["gre_v_score"] = m.group(1)
        elif m := re.match(r"gre q[: ]\s*(\d{2,3})", t):
            info["gre_q_score"] = m.group(1)
        elif m := re.match(r"gre aw[: ]\s*(\d(\.\d)?)", t):
            info["gre_aw_score"] = m.group(1)
        elif m := re.match(r"gpa[: =]?\s*(\d\.\d{1,2})", t):
            info["gpa"] = m.group(1)

    return info  # type: ignore


def main() -> None:
    """Main function: scrape, clean, save cleaned data."""
    pages_to_scrape = 10
    logging.info(f"Starting scraping for {pages_to_scrape} pages...")
    raw_data = scrape_multiple_pages(pages=pages_to_scrape)

    if not raw_data:
        logging.error("No data scraped; exiting.")
        return

    cleaned = clean_data(raw_data)
    if not cleaned:
        logging.error("No cleaned data produced; exiting.")
        return

    if not save_data(cleaned):
        logging.error("Failed to save cleaned data; exiting.")
        return

    logging.info("Scraping and cleaning completed successfully.")


if __name__ == "__main__":
    main()
