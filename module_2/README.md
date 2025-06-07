# Grad Cafe Web Scraper

**Name:** Billy Presume  
**JHED:** 790B62  

---

## Module Info

- **Module:** Module 2 – Software Concepts  
- **Assignment:** Grad Cafe Web Scraper  
- **Due Date:** *June 1, 2025* Extension

---

## Project Overview

This project is a web scraper designed to collect graduate admissions data from [The Grad Cafe](https://www.thegradcafe.com/). It uses `urllib3` and `BeautifulSoup` to fetch and parse HTML content, in compliance with the site's `robots.txt` file.

Data is extracted from the survey results table on each page, then cleaned and saved as structured JSON. Key fields include:

---

## Data Categories Collected

The scraper extracts the following data fields (when available) from each applicant entry on The Grad Cafe:

- **Program Name**
- **University**
- **Comments**
- **Date Added to The Grad Cafe**
- **Direct URL to Entry**
- **Applicant Status**
  - If **Accepted**: Acceptance Date
  - If **Rejected**: Rejection Date
- **Program Start Term and Year**
- **Citizenship Status** (International / American)
- **GRE Scores**  
  - **Combined GRE Score**
  - **GRE Verbal (V) Score**
  - **GRE Analytical Writing (AW) Score**
- **Degree Type** (Master’s or PhD)
- **GPA**

To parse and clean the data, regular expressions and string processing techniques are used for extracting GRE scores, term info, and other key attributes.

---

## Robots.txt Compliance

This project adheres to the `robots.txt` guidelines provided by [TheGradCafe](https://www.thegradcafe.com/robots.txt). Only publicly accessible pages are scraped using a respectful User-Agent and a limited number of requests.

The `robots.txt` file was reviewed on 2025-06-01 and no disallowed paths related to the `/survey` endpoint (used in this scraper) were found. If any changes are made to the site’s rules in the future, this project will be updated to remain compliant.

---

## 📁 Project Structure

```text
jhu_software_concepts/
├── module_2/
│ ├── tests/
│ │ ├── __init__.py
│ │ ├── clean_test.py
│ │ └── scraping_test.py
│ ├── __init__.py
│ ├── clean.py
│ ├── scrape.py
│ ├── Makefile
│ ├── robot_txt_screenshot.png
│ ├── requirements.txt
│ ├── pyproject.toml
│ └── README.md
├── README.md
└── .gitignore
```

## Code Structure

- Modular file organization
- Strong typing and inline documentation
- Adheres to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

## Known Issues

- None at the time of submission.

---

## Installation and Running 

- Option 1: Run clean.py file (AS INSTRUCTED IN ASSIGNMENT DESCRIPTION) (recommended)
  For instructor/grader:
    cd jhu_software_concepts/module_2
    python3 clean.py  # On Mac
    python clean.py   # On Windows
- NOTE: In clean.py in the main function change the pagepages_to_scrape variable to the desired number of pages you would like to scrape

---

## License

- This is a private project. Unauthorized distribution or use is not permitted.