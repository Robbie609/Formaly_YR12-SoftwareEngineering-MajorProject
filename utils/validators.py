# Imports
from datetime import datetime

# This function checks if a value is empty (None, empty string, or only whitespace)
def is_empty(value):
    return value is None or str(value).strip() == ""

# This function checks if a value is a valid length.
def is_valid_length(value, min_len=1, max_len=255):
    if is_empty(value):
        return False
    return min_len <= len(str(value).strip()) <= max_len

# This function cleans a text value by stripping leading and trailing whitespace.
def clean_text(value):
    return str(value).strip()

# This function checks if a value is numeric (can be converted to a float).
def is_numeric(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False

# This function validates a username and password for login, ensuring they are not empty and meet length requirements.
def validate_login(username, password):
    if is_empty(username):
        return False, "Username cannot be empty."
    if is_empty(password):
        return False, "Password cannot be empty."
    if len(clean_text(username)) < 2:
        return False, "Username is too short."
    if len(password) < 9:
        return False, "Password must be at least 9 characters."
    return True, ""

# This function validates task details, ensuring the title is not empty and the due date is in the correct format if provided.
def validate_task(title, due_date=None):
    if is_empty(title):
        return False, "Task title is required."
    if not is_valid_length(title, 1, 100):
        return False, "Task title must be between 1 and 100 characters."
    if due_date and not is_empty(due_date):
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return False, "Due date must be in YYYY-MM-DD format."
    return True, ""

def validate_not_empty(value, field_name="Field"):
    if is_empty(value):
        return False, f"{field_name} cannot be empty."
    return True, ""

# This function validates that a value is a positive number, returning an error message if it is not.
def validate_positive_number(value, field_name="Value"):
    if not is_numeric(value):
        return False, f"{field_name} must be a number."
    if float(value) <= 0:
        return False, f"{field_name} must be greater than zero."
    return True, ""

# This funcion checks if the date string is in the correct format and is a valid date, returning an error message if it is not.
def validate_date(date_str, field_name="Date"):
    if is_empty(date_str):
        return False, f"{field_name} cannot be empty."
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, f"{field_name} must be in YYYY-MM-DD format."