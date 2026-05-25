import re
from datetime import datetime


# ---------------- BASIC VALIDATION ----------------
def is_empty(value):
    return value is None or str(value).strip() == ""


def is_valid_length(value, min_len=1, max_len=255):
    if is_empty(value):
        return False
    return min_len <= len(str(value).strip()) <= max_len


# ---------------- LOGIN VALIDATION ----------------
def validate_login(username, password):
    if is_empty(username) or is_empty(password):
        return False, "Username and password cannot be empty."

    if len(password) < 4:
        return False, "Password is too short."

    return True, ""


# ---------------- TASK VALIDATION ----------------
def validate_task(title, due_date=None):
    if is_empty(title):
        return False, "Task title is required."

    if not is_valid_length(title, 1, 100):
        return False, "Task title is too long."

    # optional date validation
    if due_date and not is_empty(due_date):
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return False, "Due date must be in YYYY-MM-DD format."

    return True, ""


# ---------------- SIMPLE FORMAT HELPERS ----------------
def clean_text(value):
    return str(value).strip()


def is_numeric(value):
    try:
        float(value)
        return True
    except:
        return False