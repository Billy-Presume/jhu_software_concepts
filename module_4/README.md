# Pizza Ordering Service

**Name:** Billy Presume  
**JHED:** 790B62  

---

## Module Info

- **Module:** Module 4 – Software Concepts  
- **Assignment:** Pizza Ordering System with Unit Testing and Documentation  
- **Due Date:** *June 17, 2025*

---

## Project Overview

This project implements an **extensible and scalable pizza ordering service** in Python using a **test-driven development (TDD)** approach. The system allows customers to place and pay for orders consisting of fully customizable pizzas (crust, sauce, cheese, toppings). The cost is computed dynamically based on selected options.

The project includes:
- A robust class-based backend with `Pizza` and `Order` modules
- Full unit and integration test coverage using **pytest**
- Developer documentation generated with **Sphinx**
- Code quality enforcement using **YAPF** and **Pylint**

---

## ✅ Features

- Multiple crust, sauce, and topping combinations
- Automatic cost calculation
- Order aggregation and payment tracking
- Modular, extensible design for future expansion
- Auto-generated HTML documentation via **ReadTheDocs**

---

## 📁 Project Structure

```text
jhu_software_concepts/
└── module_4/
    ├── src/
    │   ├── __init__.py
    │   ├── pizza.py
    │   └── order.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_pizza.py
    │   ├── test_order.py
    │   └── test_integration.py
    ├── docs/
    │   ├── conf.py
    │   ├── index.rst
    │   ├── modules.rst
    │   └── _build/ (generated HTML)
    ├── requirements.txt
    ├── Makefile
    ├── README.md
    ├── pyproject.toml
    └── pytest.ini
```

---

## ⚙️ Installation & Setup

- Requires Python 3.12+

```bash
# Clone the repository
git clone <your-repo-url>
cd module_4

# Create a virtual environment and install dependencies
make venv
make install
```

---

## 🧪 Running Tests

```bash
# Run unit and integration tests
make test
```

You can also run tests directly using:

```bash
pytest -m order     # Runs tests marked with @pytest.mark.order
pytest -m pizza     # Runs tests marked with @pytest.mark.pizza
```

---

## 📐 Code Quality

```bash
# Format code
make format

# Lint code
make lint
```

---

## 📚 Documentation

```bash
# Build Sphinx docs
cd module_4/docs
make html
```

HTML output will be available in `module_4/docs/_build/html/index.html` or view it online via your [ReadTheDocs link].

---

## ✅ Requirements

The following tools are used in this project:

- pytest==8.3.5 - Unit testing framework
- sphinx>=7.0 - Documentation generator
- sphinx-rtd-theme - HTML theme for docs
- yapf==0.43.0 - Code formatter
- ylint==3.3.7 - Code linter

See `requirements.txt` and `pyproject.toml` for complete dependency details.

---

## License

This is a private project. Unauthorized distribution or use is not permitted.