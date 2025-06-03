# Grad Cafe Web Scraper

**Name:** Billy Presume  
**JHED:** 790B62  

## Module Info

- **Module:** Module 1 – Software Concepts  
- **Assignment:** Grad Cafe Web Scraper  
- **Due Date:** *[INSERT DUE DATE HERE]*

## Project Overview

This project is a web scraper designed to collect graduate admissions data from [The Grad Cafe](https://www.thegradcafe.com/). It uses `urllib3` and `BeautifulSoup` to fetch and parse HTML content, in compliance with the site's `robots.txt` file.

Data is extracted from the survey results table on each page, then cleaned and saved as structured JSON. Key fields include:

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

## Code Structure

- Modular file organization
- Strong typing and inline documentation
- Adheres to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Known Issues

- None at the time of submission.
