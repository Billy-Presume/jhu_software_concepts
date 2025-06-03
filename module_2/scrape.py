"""
Module: scrape.py
Author: Billy Presume
Created: 2025-06-01
Modified: 2025-06-03
Description: Handles web scraping from The GradCafe website.

This scraper was designed to respect TheGradCafe's robots.txt file.
Checked: https://www.thegradcafe.com/robots.txt
Date Verified: 2025-06-01

No restrictions were found for the /survey path.
Only public data is accessed, and requests are made responsibly using a custom User-Agent.
"""

import logging
from typing import Any, Optional

import urllib3
from bs4 import BeautifulSoup

HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (GradCafeScraper/1.0)"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def _fetch_page(url: str) -> Optional[str]:
    """Fetch the HTML content of a page.

    Args:
        url: URL to fetch.

    Returns:
        HTML content as string or None if failed.
    """
    http = urllib3.PoolManager()
    logging.info(f"Fetching URL: {url}")
    try:
        response = http.request("GET", url, headers=HTTP_HEADERS)
        if response.status != 200:
            logging.error(f"Failed to fetch {url} with status {response.status}")
            return None
        return response.data.decode("utf-8")
    except Exception as e:
        logging.error(f"Exception fetching {url}: {e}")
        return None


def _parse_html(html: str) -> list[dict[str, Any]]:
    """Parse raw HTML and extract raw entries.

    Args:
        html: HTML content.

    Returns:
        List of raw data dictionaries.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("table.tw-min-w-full tbody tr")
    results: list[dict[str, Any]] = []
    i = 0

    while i < len(rows):
        row = rows[i]
        if "tw-border-none" in row.get("class", []):
            i += 1
            continue

        tds = row.find_all("td")
        if len(tds) < 5:
            i += 1
            continue

        university = tds[0].get_text(strip=True)
        spans = tds[1].find_all("span")
        program_name = spans[0].get_text(strip=True) if spans else ""
        degree = spans[1].get_text(strip=True) if len(spans) > 1 else ""
        date_added = tds[2].get_text(strip=True)
        status = tds[3].get_text(strip=True)
        a_tag = row.find("a")
        url = a_tag["href"] if a_tag and "href" in a_tag.attrs else ""  # type: ignore

        # Collect tags and comments from subsequent rows
        tag_texts: list[str] = []
        comments = ""
        j = i + 1
        while j < len(rows) and "tw-border-none" in rows[j].get("class", []):
            tag_divs = rows[j].select("div.tw-inline-flex")
            if tag_divs:
                tag_texts.extend([d.get_text(strip=True) for d in tag_divs])
            else:
                comments = rows[j].get_text(strip=True)
            j += 1

        results.append({
            "university": university,
            "program_name": program_name,
            "degree": degree,
            "date_added": date_added,
            "status": status,
            "url": url,
            "tags": tag_texts,
            "comments": comments,
        })
        i = j

    logging.debug(f"Parsed {len(results)} entries")
    return results


def scrape_data(
    base_url: str = "https://www.thegradcafe.com/survey/",
    pages: int = 10,
) -> list[dict[str, Any]]:
    """Scrape multiple pages from GradCafe dynamically.

    Args:
        base_url: Base URL without page param.
        pages: Number of pages to scrape.

    Returns:
        Combined list of raw scraped entries.
    """
    all_data: list[dict[str, Any]] = []
    for page_num in range(1, pages + 1):
        url = f"{base_url}?page={page_num}&order=latest"
        logging.info(f"Scraping page {page_num}/{pages}")
        html = _fetch_page(url)
        if html is None:
            logging.warning(f"Skipping page {page_num} due to fetch failure")
            continue
        page_data = _parse_html(html)
        all_data.extend(page_data)
    logging.info(f"Total entries scraped: {len(all_data)}")
    return all_data
