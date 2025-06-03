# Makefile for module_2 - The Gradcafe Web Scraper 

# Configuration
PYTHON = python3
VENV_DIR = .venv
ACTIVATE = source $(VENV_DIR)/bin/activate
SCARAPER = clean.py
MODULE_NAME = module_2

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
	$(ACTIVATE) && $(PYTHON) $(SCARAPER)

# Code Quality
format:  ## Format code with yapf
	yapf -rip ./*.py ./tests/*.py

lint:  ## Lint with pylint
	pylint ./*.py

# Tests
test:  ## Run pytest tests
	make clean
	$(ACTIVATE) && pytest ./tests/*.py

# Clean
clean:  ## Remove __pycache__ and .pyc files
	find . -type d -name "__pycache__" -exec rm -r {} +; \
	find . -type d -name ".pytest_cache" -exec rm -r {} +; \
	find . -type f -name "*.pyc" -delete