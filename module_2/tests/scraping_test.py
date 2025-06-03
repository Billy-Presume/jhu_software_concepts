"""
Module: scraping_test.py
Author: Billy Presume
Created: 2025-06-01
Modified: 2025-06-03
Description: Unit tests for scrape.py module using pytest.
Note: Private functions (with leading underscore) are imported here **only for testing purposes**.
"""

from typing import Any, Optional
import pytest

from ..scrape import _fetch_page, _parse_html, scrape_multiple_pages  # type: ignore


@pytest.mark.parametrize(
    "status_code, data, expected", [
        (200, b"<html>content</html>", "<html>content</html>"),
        (404, b"", None),
    ]
)
def test_fetch_page(
    monkeypatch: pytest.MonkeyPatch, status_code: int, data: bytes, expected: Optional[str]
) -> None:

    class DummyResponse:

        def __init__(self, status: int, data: bytes) -> None:
            self.status = status
            self.data = data

    def dummy_request(
        method: str, url: str, headers: Optional[dict[str, str]] = None
    ) -> DummyResponse:
        return DummyResponse(status_code, data)

    monkeypatch.setattr("module_2.scrape.urllib3.PoolManager.request", dummy_request)
    result: Optional[str] = _fetch_page("http://example.com")
    assert result == expected


def test_fetch_page_exception(monkeypatch: pytest.MonkeyPatch) -> None:

    def dummy_request(method: str, url: str, headers: Optional[dict[str, str]] = None) -> None:
        raise Exception("Network error")

    monkeypatch.setattr("module_2.scrape.urllib3.PoolManager.request", dummy_request)
    result: Optional[str] = _fetch_page("http://example.com")
    assert result is None


@pytest.mark.parametrize(
    "html, expected_len", [
        ("<html><body><table><tbody></tbody></table></body></html>", 0),
    ]
)
def test_parse_html_empty(html: str, expected_len: int) -> None:
    results: list[dict[str, Any]] = _parse_html(html)
    assert len(results) == expected_len


def test_parse_html_skips_border_none_rows() -> None:
    html = """
    <html><body><table>
      <tbody>
        <tr class="tw-border-none"><td>Ignore me</td></tr>
        <tr><td>Uni</td><td><span>Program</span><span>Degree</span></td><td>2025-01-01</td><td>Accepted</td><td><a href="/link"></a></td></tr>
      </tbody>
    </table></body></html>
    """
    results = _parse_html(html)
    assert len(results) == 1
    assert results[0]["university"] == "Uni"


def test_parse_html_basic_row() -> None:
    html = """
    <html><body><table>
      <tbody>
        <tr>
          <td>University X</td>
          <td><span>Program Y</span><span>PhD</span></td>
          <td>2025-01-01</td>
          <td>Accepted on 2025-05-01</td>
          <td><a href="/survey/123"></a></td>
        </tr>
        <tr class="tw-border-none">
          <td>
            <div class="tw-inline-flex">Fall 2025</div>
            <div class="tw-inline-flex">GRE 320</div>
          </td>
        </tr>
        <tr class="tw-border-none">
          <td>Great program, excited!</td>
        </tr>
      </tbody>
    </table></body></html>
    """
    results = _parse_html(html)
    assert len(results) == 1
    entry = results[0]
    assert entry["university"] == "University X"
    assert entry["program_name"] == "Program Y"
    assert entry["degree"] == "PhD"
    assert entry["date_added"] == "2025-01-01"
    assert entry["status"] == "Accepted on 2025-05-01"
    assert entry["url"] == "/survey/123"
    assert "Fall 2025" in entry["tags"]
    assert "GRE 320" in entry["tags"]
    assert entry["comments"] == "Great program, excited!"


def test_parse_html_handles_missing_spans_and_a_tag() -> None:
    html = """
    <html><body><table>
      <tbody>
        <tr>
          <td>Uni</td>
          <td></td>
          <td>2025-01-01</td>
          <td>Rejected on 2025-02-02</td>
          <td></td>
        </tr>
      </tbody>
    </table></body></html>
    """
    results = _parse_html(html)
    assert len(results) == 1
    assert results[0]["program_name"] == ""
    assert results[0]["degree"] == ""
    assert results[0]["url"] == ""


def test_scrape_multiple_pages_success(monkeypatch: pytest.MonkeyPatch) -> None:
    pages = 2
    fake_htmls = ["<html>page1</html>", "<html>page2</html>"]
    fake_parsed = [[{"university": "U1"}], [{"university": "U2"}]]

    def fake_fetch_page(url: str) -> Optional[str]:
        return fake_htmls.pop(0) if fake_htmls else None

    def fake_parse_html(html: str) -> list[dict[str, Any]]:
        return fake_parsed.pop(0) if fake_parsed else []

    monkeypatch.setattr("module_2.scrape._fetch_page", fake_fetch_page)
    monkeypatch.setattr("module_2.scrape._parse_html", fake_parse_html)

    results = scrape_multiple_pages(base_url="http://fakeurl.com?page={}", pages=pages)
    assert len(results) == 2
    assert results[0]["university"] == "U1"
    assert results[1]["university"] == "U2"


def test_scrape_multiple_pages_skip_failed_page(monkeypatch: pytest.MonkeyPatch) -> None:
    fetch_results = ["<html>page1</html>", None, "<html>page3</html>"] # type: ignore
    parse_results = [[{"university": "U1"}], [{"university": "U3"}]]

    def fake_fetch_page(url: str) -> Optional[str]:
        return fetch_results.pop(0) # type: ignore

    def fake_parse_html(html: str) -> list[dict[str, Any]]:
        return parse_results.pop(0)

    monkeypatch.setattr("module_2.scrape._fetch_page", fake_fetch_page)
    monkeypatch.setattr("module_2.scrape._parse_html", fake_parse_html)

    results = scrape_multiple_pages(base_url="http://fakeurl.com?page={}", pages=3)
    # The None page should be skipped, so only 2 entries total
    assert len(results) == 2
    # Universities from page 1 and 3
    unis = {entry["university"] for entry in results}
    assert unis == {"U1", "U3"}
