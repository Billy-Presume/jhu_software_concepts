# Makefile for module_1 - Flask Portfolio Website

# Configuration
PYTHON = python3
VENV_DIR = .venv
ACTIVATE = source $(VENV_DIR)/bin/activate
FLASK_APP = run.py
MODULE_NAME = website

# Default: show help
.DEFAULT_GOAL := help

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Environment Setup
venv:  ## Create a virtual environment in .venv
	$(PYTHON) -m venv $(VENV_DIR)

install: venv  ## Install dependencies using uv
	$(ACTIVATE) && uv pip install -r requirements.txt

# App Running
run:  ## Run the Flask app
	make clean
	$(ACTIVATE) && FLASK_APP=$(FLASK_APP) FLASK_ENV=development FLASK_DEBUG=1 flask run

# Code Quality
format:  ## Format code with yapf
	yapf -rip src/ tests/

lint:  ## Lint with pylint
	pylint src/$(MODULE_NAME)

# Tests
test:  ## Run pytest tests
	$(ACTIVATE) && pytest

# Clean
clean:  ## Remove __pycache__ and .pyc files
	find . -type d -name "__pycache__" -exec rm -r {} +; \
	find . -type f -name "*.pyc" -delete