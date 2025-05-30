"""
Module: routes.py
Author: Billy Presume
Created: 2025-05-29
Modified: 2025-05-30
Description: Defines route endpoints using Flask Blueprints.
"""

from flask import Blueprint, render_template
from .data import get_portfolio_data

# Define the "views" blueprint for the portfolio routes
views = Blueprint('views', __name__, )

@views.route('/')
def home():
    """
    Renders the homepage with personal and professional portfolio data.

    Returns:
        Response: Rendered index.html template populated with structured data.
    """
    context = get_portfolio_data()
    return render_template("index.html", **context)
