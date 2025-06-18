# Makefile for module_5 - Database SQL Data Analysis (Modified w/ linting, formatting, and dependency graph)

# Configuration
PYTHON = python3
VENV_DIR = .venv

# Detect OS to set proper activation command and open command
ifeq ($(OS),Windows_NT)
	ACTIVATE = $(VENV_DIR)\Scripts\activate
	OPEN_CMD = start
	SHELL := powershell.exe
else
	ACTIVATE = . $(VENV_DIR)/bin/activate
	OPEN_CMD = xdg-open
	ifeq ($(shell uname),Darwin)
		OPEN_CMD = open
	endif
	SHELL := /bin/bash
endif

APP = app.py
MODULE_NAME = website

# Default: show help
.DEFAULT_GOAL := help

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Environment Setup
venv:  ## Create a virtual environment in .venv
	$(PYTHON) -m venv $(VENV_DIR)

install: venv  ## Install dependencies from requirements.txt
	@if [ "$(OS)" = "Windows_NT" ]; then \
		powershell -Command "& { . $(VENV_DIR)/Scripts/Activate.ps1; pip install -r requirements.txt }"; \
	else \
		. $(VENV_DIR)/bin/activate && pip install -r requirements.txt; \
	fi

# Code Quality
format:  ## Format code with yapf
	@if [ "$(OS)" = "Windows_NT" ]; then \
		powershell -Command "& { . $(VENV_DIR)/Scripts/Activate.ps1; yapf -rip src/ tests/ }"; \
	else \
		. $(VENV_DIR)/bin/activate && yapf -rip src/ tests/; \
	fi

lint:  ## Lint with pylint
	@if [ "$(OS)" = "Windows_NT" ]; then \
		powershell -Command "& { . $(VENV_DIR)/Scripts/Activate.ps1; pylint src/ }"; \
	else \
		. $(VENV_DIR)/bin/activate && pylint src/; \
	fi

# App Running
run: clean  ## Run the Flask app
	@if [ "$(OS)" = "Windows_NT" ]; then \
		powershell -Command "& { . $(VENV_DIR)/Scripts/Activate.ps1; \
		$env:FLASK_APP='$(APP)'; $env:FLASK_ENV='development'; $env:FLASK_DEBUG='1'; flask run }"; \
	else \
		. $(VENV_DIR)/bin/activate && FLASK_APP=$(APP) FLASK_ENV=development FLASK_DEBUG=1 flask run; \
	fi

# Tests
test:  ## Run pytest tests
	@if [ "$(OS)" = "Windows_NT" ]; then \
		powershell -Command "& { . $(VENV_DIR)/Scripts/Activate.ps1; pytest tests/ }"; \
	else \
		. $(VENV_DIR)/bin/activate && pytest tests/; \
	fi

# Clean
clean:  ## Remove __pycache__, .pyc, and pytest cache files
	@echo "Cleaning up..."
	@if [ "$(OS)" = "Windows_NT" ]; then \
		powershell -Command "Get-ChildItem -Recurse -Include __pycache__,*.pyc -Directory | Remove-Item -Recurse -Force; Remove-Item -Recurse -Force .pytest_cache"; \
	else \
		find . -type d -name "__pycache__" -exec rm -r {} +; \
		find . -type d -name ".pytest_cache" -exec rm -r {} +; \
		find . -type f -name "*.pyc" -delete; \
	fi

# Dependency graph for app.py
dependency:
	pydeps app.py -o dependency.svg
	@echo "Opening dependency.svg..."
	@if [ "$(OS)" = "Windows_NT" ]; then \
		start dependency.svg; \
	elif [ "$(shell uname)" = "Darwin" ]; then \
		open dependency.svg; \
	else \
		xdg-open dependency.svg; \
	fi

# Phony targets
.PHONY: help venv install run format lint test clean