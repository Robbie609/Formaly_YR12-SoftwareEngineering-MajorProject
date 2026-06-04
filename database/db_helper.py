import sqlite3
import os

DB_PATH = "database/formaly.db"

def get_db_connection():
    """Establishes a connection to the SQLite database with Row factory enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the attendees table and seeds it if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            plus_one INTEGER DEFAULT 0,
            paid INTEGER DEFAULT 0,
            attendance INTEGER DEFAULT 0
        );
    """)
    
    # Check if data already exists to prevent duplicate seeding
    cursor.execute("SELECT COUNT(*) FROM attendees")
    if cursor.fetchone() == 0:
        students = [
            "Socrates Amistoso", "Hayden Chan", "Raymond Chuang", "Rigved Gambhir", 
            "Harrison Hsieh", "Mitchell Kalajzich", "Jim Ke", "Kristian Lee", 
            "Ethan Leung", "Kyan Setiadi", "Benny Tan", "Aarya Udupa", 
            "Leo Wang", "Tony Xia", "Max Zheng"
        ]
        unpaid_list = {"Tony Xia", "Benny Tan", "Raymond Chuang", "Hayden Chan"}
        no_plus_one_list = {"Rigved Gambhir"}
        
        for name in students:
            paid = 0 if name in unpaid_list else 1
            plus_one = 0 if name in no_plus_one_list else 1
            cursor.execute(
                "INSERT INTO attendees (name, plus_one, paid, attendance) VALUES (?, ?, ?, 0)",
                (name, plus_one, paid)
            )
        conn.commit()
    conn.close()

def execute_update(query, params=()):
    """Executes a write operation and commits immediately to guarantee persistence."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_query(query, params=()):
    """Executes a read query and returns all matching rows."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows