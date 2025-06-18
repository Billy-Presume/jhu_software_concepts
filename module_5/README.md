# Grad Cafe Web Scraper

**Name:** Billy Presume  
**JHED:** 790B62  

---

## Module Info

- **Module:** Module 3 – Software Concepts  
- **Assignment:** Grad Cafe Data Analysis  
- **Due Date:** *June 8, 2025*

---

## Project Overview

This project involves loading scraped and cleaned data from Grad Café into a PostgreSQL database, then using SQL queries to analyze submission trends and answer specific questions. The analysis results are displayed on a Flask webpage, and the project includes a reflection on the limitations of using anonymous, user-submitted data sources like Grad Café.

The data extracted from the survey results table on each page, then cleaned and saved as structured JSON. Key fields include:

---

## Data Categories Collected

The scraper extracted the following data fields (when available) from each applicant entry on The Grad Cafe and loaded into the "applicants" table in the postgresql gradcafe_db database:

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

---

## 📁 Project Structure

```text
jhu_software_concepts/
├── module_3/
│ ├── src/
│ │ ├── utils/
│ │ │  ├── __init__.py
│ │ │  ├── database.py
│ │ │  ├── sql-query_sanitizer.py
│ │ ├── website
│ │ │  ├── static/
│ │ │  │  ├── css/
│ │ │  │  │  ├── custom.css
│ │ │  │  │  └── styles.css
│ │ │  │  ├── gradcafe_applicant_data/
│ │ │  │  │  ├── applicant_data_2.json
│ │ │  │  │  └── applicant_data.json
│ │ │  │  └── (favicon images)
│ │ │  └── templates/
│ │ │     ├── components/
│ │ │     │ ├── _navbar.html
│ │ │     │ └── _footer.html
│ │ │     ├── base.html
│ │ │     └── index.html
│ │ ├── __init__.py
│ │ ├── load_data.py
│ │ ├── query_data.py
│ │ └── routes.py
│ ├── tests/
│ ├── app.py
│ ├── .env
│ ├── .pylintrc
│ ├── limitations.pdf
│ ├── Makefile
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

- Navigate to mofule_3 in the terminal and run: pip install -r requirements.txt

- **FIRST**: Create a .env file in the module_3 root directory with the following variables and respective value:
  - **export DB_NAME=gradcafe_db**
  - **export DB_USER=your_username**
  - **export DB_PASSWORD=your_password**
  - **export DB_HOST=localhost**
  - **export DB_PORT=5432**
  - **export LOAD_DATA_ON_FIRST_RUN=1**

- **SECOND**: Make sure the applicant JSON data file(s) you want to add to the database are in the gradcafe_applicant_data directory.

- **THIRD**: If you don't have a database with the DB_NAME you added in the .env you created with a table name "applicants". Make sure to create one. In the terminal once you have postgresql running:
    - 1) CREATE DATABASE gradcafe_db;
    - 2) CREATE USER your_username WITH PASSWORD 'your_password';
    - 3) GRANT ALL PRIVILEGES ON DATABASE gradcafe_db TO your_username;

- **FOURTH**: Once your data is loaded in your applicants table, verify that the file names in the load_data.py and routes.py for the variables DATA_FILE and DATA_FILE_2 match yours in the gradcafe_applicant_data directory. And if you only have one file comment out line 38: load_applicants(connection, DATA_FILE_2) in the routes.py file.

- **FIFTH**: CRITICAL: If this is your VERY FIRST first time running the program, uncomment line 100: load_if_first_time() in the routes.py file. After the first time, comment out line 100 again before running the program again or else if you reloaded the window before commenting it out it will load the same data in you applicants table in your gradcafe_db and cause duplicates of eveything. Also, the queries are in the routes.py instead ot the query_data.py file.

- **SIXTH**: After AND ONLY after you make sure all the previous steps are successfully completed, navigate to module_3 in the terminal:
  - Run app.py file (recommended)
    For instructor/grader:
      cd jhu_software_concepts/module_3
      python3 app.py  # On Mac
      python app.py   # On Windows

---

## License

- This is a private project. Unauthorized distribution or use is not permitted.