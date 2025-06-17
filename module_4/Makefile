# Makefile for module_4 - Pizza Ordering Service

# Configuration
PYTHON = python3
VENV_DIR = .venv
ACTIVATE = source $(VENV_DIR)/bin/activate
MODULE_NAME = src

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

# Tests
test:  ## Run pytest tests
	$(ACTIVATE) && pytest tests/

# Clean
clean:  ## Remove __pycache__, .pyc, and pytest cache files
	find . -type d -name "__pycache__" -exec rm -r {} +; \
	find . -type d -name ".pytest_cache" -exec rm -r {} +; \
	find . -type f -name "*.pyc" -delete