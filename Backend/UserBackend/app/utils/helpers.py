import re
from datetime import datetime
from flask import jsonify


# Example function to validate email format
def validate_email(email):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email)


# Example function for formatting dates
def format_date(date_string):
    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        return date_object.strftime("%B %d, %Y")
    except ValueError:
        return None


# Function to standardize error response
def error_response(message, status_code):
    return jsonify({"error": message}), status_code
