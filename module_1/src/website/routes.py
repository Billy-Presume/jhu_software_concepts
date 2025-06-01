"""
Module: routes.py
Author: Billy Presume
Created: 2025-05-29
Modified: 2025-06-1
Description: Defines route endpoints using Flask Blueprints.
"""

import smtplib
from email.mime.text import MIMEText
import re
from flask import Blueprint, render_template, request, redirect, flash
from .data import get_portfolio_data

# Define the "views" blueprint for the portfolio routes
views = Blueprint(
    'views',
    __name__,
)

# Load portfolio data from external source
context = get_portfolio_data()


# Handles all requests to the website as they are sections
@views.route('/')
@views.route('/home')
@views.route('/#profile')
@views.route('/profile')
@views.route('/#experience')
@views.route('/experience')
@views.route('/#recognition')
@views.route('/recognition')
@views.route('/#projects')
@views.route('/projects')
@views.route('/#contact')
@views.route('/contact')
def home():
    """
    Renders the homepage with personal and professional portfolio data.

    Returns:
        Response: Rendered index.html template populated with structured data.
    """
    return render_template("index.html", **context)


# List of prohibited words for basic profanity filtering
# I added this just in case, better safe than sorry
BAD_WORDS = {
    "bad_word_example_1", "bad_word_example_2", "bad_word_example_3", "bad_word_example_4", "bad_word_example_5", "bad_word_example_6",
}


def contains_profanity(text: str) -> bool:
    """
    Checks whether the provided text contains any profane or inappropriate words.

    Args:
        text (str): The input string to be checked.

    Returns:
        bool: True if profanity is detected, False otherwise.
    """
    text = text.lower()
    return any(bad_word in text for bad_word in BAD_WORDS)


@views.route('/send_message', methods=['POST'])
def send_message():
    """
    Processes the contact form submission. Validates input fields for correctness
    and profanity, and sends the message to the website owner's email if valid.

    Returns:
        Response: Redirects the user back to the contact section with success or
        error messages flashed.
    """
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    # Validate email format
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash("Please provide a valid email address.", "error")
        return redirect('/#contact')

    # Validate subject and message content
    if not subject or contains_profanity(subject):
        flash("Subject cannot be empty or contain inappropriate language.", "error")
        return redirect('/#contact')

    if not message or contains_profanity(message):
        flash("Message cannot be empty or contain inappropriate language.", "error")
        return redirect('/#contact')

    try:
        # Email configuration
        sender_email = "billypresume@gmail.com"  # Will update to business email when I create one
        sender_password = "vajy hyea kksv iemu"  # Will be moved to .env but I'm in a rush, it's 3AM right now
        receiver_email = "billy.g.presume@gmail.com"

        # Prepare the email content
        msg = MIMEText(f"From: {email}\n\n{message}")
        msg['Subject'] = f"Portfolio Contact: {subject}"
        msg['From'] = email
        msg['To'] = receiver_email

        # Send email using Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(email, receiver_email, msg.as_string())

        flash("Your message has been sent successfully!", "success")
    except Exception as e:
        print("Email error:", e)
        flash("An error occurred while sending your message. Please try again later.", "error")

    return redirect('/#contact')
