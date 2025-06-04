"""
Module: clean.py
Author: Billy Presume
Created: 2025-06-01
Modified: 2025-06-03
Description: Processes raw scraped GradCafe data and converts it into structured clean format,
             and supports loading/saving cleaned data with graceful error handling.

This scraper was designed to respect TheGradCafe's robots.txt file.
Checked: https://www.thegradcafe.com/robots.txt
Date Verified: 2025-06-01

No restrictions were found for the /survey path.
Only public data is accessed, and requests are made responsibly using a custom User-Agent.
"""

import json
import logging
import re
from typing import Any, Optional
from datetime import datetime

import urllib3
from scrape import scrape_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def check_robots_txt_compliance() -> bool:
    """Checks whether scraping /survey is allowed for generic User-agent (*).

    Returns:
        True if allowed, False otherwise.
    """
    ROBOTS_URL = "https://www.thegradcafe.com/robots.txt"
    TARGET_PATHS = ["/", "/survey"]
    http = urllib3.PoolManager()

    logging.info("🔍 Checking robots.txt for scraping permissions...")

    try:
        response = http.request("GET", ROBOTS_URL)
        if response.status != 200:
            logging.warning("⚠️ Failed to fetch robots.txt. Status code: %d", response.status)
            return False

        lines = response.data.decode("utf-8").splitlines()
        in_generic_block = False
        disallowed: list[str] = []
        allowed: list[str] = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.lower().startswith("user-agent:"):
                ua = line.split(":", 1)[1].strip().lower()
                in_generic_block = (ua == "*")
                continue

            if in_generic_block:
                if line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        disallowed.append(path)
                elif line.lower().startswith("allow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        allowed.append(path)

        logging.info("📅 robots.txt checked on %s", datetime.now().strftime("%Y-%m-%d"))
        logging.info("📄 Disallowed (User-agent: *):")
        for path in disallowed:
            logging.info("   🚫 %s", path)
        logging.info("📄 Allowed (User-agent: *):")
        for path in allowed:
            logging.info("   ✅ %s", path)

        # If /survey is disallowed and not explicitly allowed, return False
        for target in TARGET_PATHS:
            for block in disallowed:
                if target.startswith(block):
                    logging.error("❌ Scraping disallowed: '%s' blocks '%s'", block, target)
                    return False

        logging.info("✅ /survey is allowed under generic robots.txt rules.")
        return True

    except Exception as e:
        logging.exception("⚠️ Error while checking robots.txt: %s", str(e))
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


def save_data(data: list[dict[str, Any]], filename: str = "applicant_data.json") -> bool:
    """Saves cleaned data to a JSON file.

    Overwrites the file if it already exists. Validates that data is a list of dictionaries.
    Logs success or detailed failure information.

    Args:
        data: Cleaned data list.
        filename: Output JSON filename.

    Returns:
        True if successful, False otherwise.
    """
    # Defensive runtime check — still valuable even if statically annotated
    if not all(isinstance(item, dict) for item in data):  # type: ignore # noqa: B007
        logging.error("Invalid data format: all items must be dictionaries.")
        return False

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        logging.info(f"Saved cleaned data to {filename}")
        return True
    except OSError as e:
        logging.error(f"File system error when saving to {filename}: {e}", exc_info=True)
        return False
    except TypeError as e:
        logging.error(f"Data serialization error: {e}", exc_info=True)
        return False
    except Exception as e:
        logging.error(f"Unexpected error while saving to {filename}: {e}", exc_info=True)
        return False


def load_data(filename: str = "applicant_data.json") -> list[dict[str, Any]] | None:
    """Loads JSON data from a file.

    Validates that the loaded data is a list of dictionaries.
    Logs success or detailed failure information.

    Args:
        filename: Path to the JSON file to load.

    Returns:
        A list of dictionaries if successful, None otherwise.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list) or not all(isinstance(item, dict)
                                                 for item in data):  # type: ignore
            logging.error(f"Invalid data format in {filename}: Expected a list of dictionaries.")
            return None

        logging.info(f"Successfully loaded data from {filename}")
        return data  # type: ignore

    except FileNotFoundError:
        logging.warning(f"File not found: {filename}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error in {filename}: {e}", exc_info=True)
        return None
    except OSError as e:
        logging.error(f"File system error when reading {filename}: {e}", exc_info=True)
        return None
    except Exception as e:
        logging.error(f"Unexpected error while loading from {filename}: {e}", exc_info=True)
        return None


def main() -> None:
    """Main function: scrape, clean, save cleaned data."""
    if not check_robots_txt_compliance():
        logging.critical("🚫 Scraping is not permitted by robots.txt. Exiting.")
        return

    pages_to_scrape = 1000  # Liv/Francisco: Change to less for grading if you would like
    logging.info(f"🔍 Starting scraping for {pages_to_scrape} pages...")
    raw_data = scrape_data(pages=pages_to_scrape)

    if not raw_data:
        logging.error("📄 No data scraped; exiting.")
        return

    cleaned = clean_data(raw_data)
    if not cleaned:
        logging.error("⚠️ No cleaned data produced; exiting.")
        return

    if not save_data(cleaned):
        logging.error("⚠️ Failed to save cleaned data; exiting.")
        return

    logging.info("✅ Scraping and cleaning completed successfully.")


if __name__ == "__main__":
    main()
