"""
Module: conf.py
Author: Billy Presume
Created: 2025-06-17
Modified: 2025-06-17
Description: Sphinx configuration file for generating HTML documentation
for the Pizza Ordering Service project. Adjusts the Python path to
include the `src` directory, and enables Napoleon for Google-style
docstrings.
"""

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# Project information
project = 'Pizza Ordering Service'
author = 'Billy Presume'
release = '1.0'
copyright = '2025'

# Sphinx extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

# Templates and static paths
templates_path = ['_templates']
html_static_path = ['_static']

# HTML theme
html_theme = 'alabaster'  # You can change to 'sphinx_rtd_theme' if needed

# Source file settings
exclude_patterns = []
