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


context = get_portfolio_data()

@views.route('/')
@views.route('/#home')
# @views.route('/#profile')
# @views.route('/#experience')
# @views.route('/#recognition')
# @views.route('/#contact')
def home():
    """
    Renders the homepage with personal and professional portfolio data.

    Returns:
        Response: Rendered index.html template populated with structured data.
    """
    # print(f"Bio data: {context.get("bio")}")
    return render_template("index.html", **context)
