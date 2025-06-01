# Flask Portfolio Website

This is a private portfolio website built using [Flask](https://flask.palletsprojects.com/). The site demonstrates web development concepts using modular and maintainable Python code. It is intended for local development and educational purposes.

1. Billy Presume -  JHED ID: 790B62
2. Module 1 Assignment: Personal Website (May 25 by 11:59pm) [NOTE: I got an extension for module 1 until June 1 by 11:59 EST]

---

## 📁 Project Structure

```text
jhu_software_concepts/
├── module_1/
│ ├── src/
│ │ ├── utils/
│ │ └── website/
│ │ ├── static/
│ │ │ ├── assets/
│ │ │ ├── css/
│ │ │ └── js/
│ │ ├── templates/
│ │ │ ├── components/
│ │ │ │ ├── _profile.html
│ │ │ │ ├── _experience.html
│ │ │ │ ├── _recognition.html
│ │ │ │ └── _contact.html
│ │ │ ├── base.html
│ │ │ └── index.html
│ │ ├── init.py
│ │ ├── main.py
│ │ ├── data.py
│ │ ├── models.py
│ │ └── routes.py
│ ├── tests/
│ ├── Makefile
│ ├── requirements.txt
│ ├── pyproject.toml
│ └── README.md
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

These instructions will help you set up and run the portfolio website locally.

### 🔧 Prerequisites

- Python 3.8 or higher
- One of the following Python package managers:
  - [`uv`](https://github.com/astral-sh/uv) (recommended)
  - `pip`
  - `pipenv`
  - `poetry`

---

## 📦 Installation

Navigate to the root of the project (`jhu_software_concepts/module_1`) before installing dependencies.

### Using `uv` (recommended)

```bash
cd jhu_software_concepts/module_1
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

### Using `pip`

cd jhu_software_concepts/module_1
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

If you prefer pipenv or poetry, install dependencies using:
    - "pipenv install"
    - "poetry install"

▶️ Running the Application

All commands should be executed from within the jhu_software_concepts/module_1 directory.
Option 1: Using the Makefile (recommended)

If you're using a virtual environment, simply run:
    make run

🔧 Note:

The Makefile assumes a virtual environment is active and may reference .venv. If you're not using a virtual environment, you must update the Makefile accordingly.

Example line to modify in the Makefile:
    run:
        . .venv/bin/activate && flask --app src/website run
Adjust this based on your setup or Python path.

Option 2: Run Flask manually
If you're unfamiliar with Makefiles or encounter issues:
    cd jhu_software_concepts/module_1
    export FLASK_APP=src/website  # On Windows: set FLASK_APP=src/website
    flask run

🌐 Access the Application

Once running, the site will be available at:
    http://127.0.0.1:5000/

⚙️ Customization

    HTML Templates: Modify layout and page structure in src/website/templates/.

    Components: Each page section is a component under templates/components/.

    Static Assets: Stylesheets, JavaScript, and media assets are in src/website/static/.

    Routing & Logic: Business logic and routes are handled in main.py, routes.py, and supporting modules under src/website/.


🔐 License

This is a private project. Unauthorized distribution or use is not permitted.