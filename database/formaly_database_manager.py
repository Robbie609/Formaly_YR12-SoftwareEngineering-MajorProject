# All database access goes through this file.
# No page file should import sqlite3 directly.

# Imports
import sqlite3
import hashlib
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# This connects the database file to a variable for use in the functions below
DB_PATH = resource_path("database/formaly.db")

# This function creates a connection to the database and allows access by column name
def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # all rows accessible by column name
    return conn

# This function hashes a password using SHA-256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

# This function initializes the database by creating all necessary tables if they do not already exist.
def init_db():
    conn = _connect()
    cur  = conn.cursor()

    # accounts 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            Account_Id      INTEGER PRIMARY KEY AUTOINCREMENT,
            Username        TEXT    NOT NULL UNIQUE,
            Password_Hashed TEXT    NOT NULL,
            School          TEXT    NOT NULL DEFAULT '',
            Formal_Name     TEXT             DEFAULT '',
            Role            TEXT    NOT NULL CHECK(Role IN ('admin','planner','helper'))
        )
    """)

    # tasks 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title            TEXT    NOT NULL,
            description      TEXT,
            priority         TEXT    NOT NULL DEFAULT 'Medium',
            category         TEXT,
            status           TEXT    NOT NULL DEFAULT 'Pending',
            due_date         TEXT,
            assigned_section TEXT
        )
    """)

    # attendees
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendees (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT    NOT NULL UNIQUE,
            plus_one   INTEGER DEFAULT 0,
            paid       INTEGER DEFAULT 0,
            attendance INTEGER DEFAULT 0
        )
    """)

    # venues
    cur.execute("""
        CREATE TABLE IF NOT EXISTS venues (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT    NOT NULL,
            address        TEXT,
            capacity       INTEGER DEFAULT 0,
            estimated_cost REAL    DEFAULT 0,
            notes          TEXT,
            status         TEXT    DEFAULT 'Shortlisted'
        )
    """)

    # EppingFormalData
    cur.execute("""
        CREATE TABLE IF NOT EXISTS EppingFormalData (
            formal_id        TEXT PRIMARY KEY,
            formal_name      TEXT,
            school           TEXT,
            budget           INTEGER DEFAULT 0,
            expenses         INTEGER DEFAULT 0,
            people_invited   INTEGER DEFAULT 0,
            people_attended  INTEGER DEFAULT 0,
            issues_occured   INTEGER DEFAULT 0,
            issues_resolved  INTEGER DEFAULT 0,
            feedback         TEXT
        )
    """)

    # feedback
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Feedback (
            feedback_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            overall_feedback TEXT,
            improvements     TEXT
        )
    """)

    conn.commit()
    conn.close()

# This function retrieves a user from the accounts table based on the provided username and password, returning the user's row if found or None if not.
def get_user(username: str, password: str):
    """
    Return the accounts row for username + password, or None.
    Row columns: Account_Id, Username, Password_Hashed, School, Formal_Name, Role
    """
    conn = _connect()
    cur  = conn.cursor()
    pw_hash = hash_password(password)
    cur.execute(
        "SELECT * FROM accounts WHERE LOWER(Username) = LOWER(?) AND Password_Hashed = ?",
        (username, pw_hash)
    )
    row = cur.fetchone()
    conn.close()
    return row

# This function gets all tasks from the tasks table, ordered by task_id
def get_all_tasks():
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY task_id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

# This function retrieves tasks from the tasks table that are assigned to a specific section, ordered by due date.
def get_tasks_by_section(section: str):
    conn = _connect()
    cur  = conn.cursor()
    cur.execute(
        "SELECT * FROM tasks WHERE LOWER(assigned_section) = LOWER(?) ORDER BY due_date ASC",
        (section,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

# This function gets the count of tasks that are not marked as 'Completed' in the tasks table.
def get_pending_task_count():
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tasks WHERE status != 'Completed'")
    count = cur.fetchone()[0]
    conn.close()
    return count

# This function adds a new task to the tasks table with the provided details, defaulting the status to "Pending" if not specified.
def add_task(title, description, priority, category, due_date, assigned_section,
             status="Pending"):
    # Column order matches real DB: status comes before due_date
    conn = _connect()
    cur  = conn.cursor()
    cur.execute(
        """INSERT INTO tasks
               (title, description, priority, category, status, due_date, assigned_section)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (title, description, priority, category, status, due_date, assigned_section)
    )
    conn.commit()
    conn.close()

# This function updates an existing task in the tasks table with the details
def update_task(task_id, title, description, priority, category, due_date,
                assigned_section, status=None):
    conn = _connect()
    cur  = conn.cursor()
    if status is not None:
        cur.execute(
            """UPDATE tasks
               SET title=?, description=?, priority=?, category=?,
                   status=?, due_date=?, assigned_section=?
               WHERE task_id=?""",
            (title, description, priority, category, status, due_date,
             assigned_section, task_id)
        )
    else:
        cur.execute(
            """UPDATE tasks
               SET title=?, description=?, priority=?, category=?,
                   due_date=?, assigned_section=?
               WHERE task_id=?""",
            (title, description, priority, category, due_date,
             assigned_section, task_id)
        )
    conn.commit()
    conn.close()

# This function marks a task as complete by updating its status to "Completed" in the tasks table.
def mark_task_complete(task_id):
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("UPDATE tasks SET status='Completed' WHERE task_id=?", (task_id,))
    conn.commit()
    conn.close()

# This function deletes a task from the tasks table based on the provided task_id.
def delete_task(task_id):
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE task_id=?", (task_id,))
    conn.commit()
    conn.close()

# This gets all attendees from the attendees table and returns them ordered by name
def get_all_attendees(search_query=""):
    conn = _connect()
    cur  = conn.cursor()
    if search_query:
        cur.execute(
            "SELECT * FROM attendees WHERE name LIKE ? ORDER BY name ASC",
            (f"%{search_query}%",)
        )
    else:
        cur.execute("SELECT * FROM attendees ORDER BY name ASC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

# This function updates an existing attendee in the attendees table
def update_attendance(student_id, status):
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("UPDATE attendees SET attendance=? WHERE id=?", (status, student_id))
    conn.commit()
    conn.close()

# THis function updates the payment status of an attendee in the attendees table
def update_payment(student_id, status):
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("UPDATE attendees SET paid=? WHERE id=?", (status, student_id))
    conn.commit()
    conn.close()

# This function updates the plus one status of an attendee in the attendees table
def update_plus_one(student_id, status):
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("UPDATE attendees SET plus_one=? WHERE id=?", (status, student_id))
    conn.commit()
    conn.close()

# This gets attendance statistics from the attendees table
def get_attendance_stats():
    conn  = _connect()
    cur   = conn.cursor()
    stats = {}

    for key, sql in [
        ("total",     "SELECT COUNT(*) FROM attendees"),
        ("present",   "SELECT COUNT(*) FROM attendees WHERE attendance=1"),
        ("paid",      "SELECT COUNT(*) FROM attendees WHERE paid=1"),
        ("unpaid",    "SELECT COUNT(*) FROM attendees WHERE paid=0"),
        ("plus_ones", "SELECT COUNT(*) FROM attendees WHERE plus_one=1"),
    ]:
        cur.execute(sql)
        stats[key] = cur.fetchone()[0]

    conn.close()
    return stats

# This function gets all venues from the venues table and returns them ordered by name
def get_all_venues():
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM venues ORDER BY name ASC")
    rows = cur.fetchall()
    conn.close()
    return rows

# This function gets the count of venues in the venues table
def get_venue_count():
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM venues")
    count = cur.fetchone()[0]
    conn.close()
    return count

# This function updates the details of a venue in the venues table
def update_venue_status(venue_id, status):
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("UPDATE venues SET status=? WHERE id=?", (status, venue_id))
    conn.commit()
    conn.close()

# This function gets the data on the demo formal from the EppingFormalData table
def get_formal_data():
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM EppingFormalData LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else {}

# This function updates the formal data in the EppingFormalData table.
def update_formal_data(formal_id, **fields):
    if not fields:
        return
    set_clause = ", ".join(f"{k}=?" for k in fields)
    values = list(fields.values()) + [formal_id]
    conn = _connect()
    cur  = conn.cursor()
    cur.execute(f"UPDATE EppingFormalData SET {set_clause} WHERE formal_id=?", values)
    conn.commit()
    conn.close()

# This function adds feedback to the Feedback table
def add_feedback(overall_feedback, improvements):
    conn = _connect()
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO Feedback (overall_feedback, improvements) VALUES (?, ?)",
        (overall_feedback, improvements)
    )
    conn.commit()
    conn.close()

# This function retrieves all feedback entries from the Feedback table
def get_all_feedback():
    conn = _connect()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM Feedback ORDER BY feedback_id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows