# Makefile for module_3 - Database SQL Data Analysis

# Configuration
PYTHON = python3
VENV_DIR = .venv
ACTIVATE = . $(VENV_DIR)/bin/activate
APP = app.py
MODULE_NAME = website

# Default: show help
.DEFAULT_GOAL := help

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Environment Setup
venv:  ## Create a virtual environment in .venv
	$(PYTHON) -m venv $(VENV_DIR)

install: venv  ## Install dependencies from requirements.txt
	$(ACTIVATE) && pip install -r requirements.txt

# Code Quality
format:  ## Format code with yapf
	$(ACTIVATE) && yapf -rip src/ tests/

lint:  ## Lint with pylint
	$(ACTIVATE) && pylint src/

# App Running
run:  ## Run the Flask app
	make clean
	$(ACTIVATE) && FLASK_APP=$(APP) FLASK_ENV=development FLASK_DEBUG=1 flask run

# Tests
test:  ## Run pytest tests
	$(ACTIVATE) && pytest tests/

# Clean
clean:  ## Remove __pycache__, .pyc, and pytest cache files
	find . -type d -name "__pycache__" -exec rm -r {} +; \
	find . -type d -name ".pytest_cache" -exec rm -r {} +; \
	find . -type f -name "*.pyc" -delete

# Phony targets
.PHONY: help venv install run format lint test clean