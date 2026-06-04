import sqlite3
import hashlib

DB_PATH = "database/formaly.db"

# ---------------- CONNECTION ----------------
def connect():
    return sqlite3.connect(DB_PATH)


# ---------------- PASSWORD HASHING ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- SETUP ----------------
def init_db():
    con = connect()
    cur = con.cursor()

    # Accounts table (LOGIN)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT UNIQUE NOT NULL,
        Password_Hashed TEXT NOT NULL,
        Role TEXT NOT NULL
    )
    """)

    # Tasks table (CORE SYSTEM)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT,
        category TEXT,
        due_date TEXT,
        assigned_section TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        plus_one INTEGER DEFAULT 0,
        paid INTEGER DEFAULT 0,
        attendance INTEGER DEFAULT 0
    )
    """)
    con.commit()

    cur.execute("SELECT COUNT(*) FROM Accounts")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO Accounts (Username, Password_Hashed, Role) VALUES (?, ?, ?)",
                    ("admin", hash_password("password"), "Admin"))
        cur.execute("INSERT INTO Accounts (Username, Password_Hashed, Role) VALUES (?, ?, ?)",
                    ("student", hash_password("password"), "Attendee"))
        cur.execute("INSERT INTO Accounts (Username, Password_Hashed, Role) VALUES (?, ?, ?)",
                    ("planner", hash_password("password"), "Planner"))
        cur.execute("INSERT INTO Accounts (Username, Password_Hashed, Role) VALUES (?, ?, ?)",
                    ("support", hash_password("password"), "Support"))
        con.commit()

    con.close()


# ---------------- ACCOUNTS ----------------
def get_user(username, password):
    con = connect()
    cur = con.cursor()

    password_hash = hash_password(password)

    cur.execute("""
        SELECT * FROM Accounts
        WHERE LOWER(Username)=LOWER(?)
        AND Password_Hashed=?
    """, (username, password_hash))

    user = cur.fetchone()
    con.close()
    return user


# ---------------- TASKS ----------------
def get_all_tasks():
    con = connect()
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("SELECT * FROM Tasks ORDER BY task_id DESC")
    tasks = cur.fetchall()

    con.close()
    return tasks


def add_task(title, description, priority, category, due_date, assigned_section):
    con = connect()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO Tasks (title, description, priority, category, due_date, assigned_section)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, description, priority, category, due_date, assigned_section))

    con.commit()
    con.close()


def update_task(task_id, title, description, priority, category, due_date, assigned_section):
    con = connect()
    cur = con.cursor()

    cur.execute("""
        UPDATE Tasks
        SET title=?, description=?, priority=?, category=?, due_date=?, assigned_section=?
        WHERE task_id=?
    """, (title, description, priority, category, due_date, assigned_section, task_id))

    con.commit()
    con.close()


def delete_task(task_id):
    con = connect()
    cur = con.cursor()

    cur.execute("DELETE FROM Tasks WHERE task_id=?", (task_id,))

    con.commit()
    con.close()


def mark_task_complete(task_id):
    con = connect()
    cur = con.cursor()

    cur.execute("""
        UPDATE Tasks
        SET status='Completed'
        WHERE task_id=?
    """, (task_id,))

    con.commit()
    con.close()

DB_PATH = "database/formaly.db"

def get_all_attendees(search_query=""):
    """Fetches attendees via SQLite, strictly for Tkinter Treeview."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if search_query:
        c.execute("SELECT * FROM attendees WHERE name LIKE ? ORDER BY name ASC", (f"%{search_query}%",))
    else:
        c.execute("SELECT * FROM attendees ORDER BY name ASC")
        
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

def update_attendance(student_id, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE attendees SET attendance = ? WHERE id = ?", (status, student_id))
    conn.commit()
    conn.close()

def update_payment(student_id, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE attendees SET paid = ? WHERE id = ?", (status, student_id))
    conn.commit()
    conn.close()

def update_plus_one(student_id, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE attendees SET plus_one = ? WHERE id = ?", (status, student_id))
    conn.commit()
    conn.close()

def get_attendance_stats():
    conn = sqlite3.connect("formaly.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM attendees")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendees WHERE attendance = 1")
    present = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendees WHERE paid = 1")
    paid = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendees WHERE paid = 0")
    unpaid = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendees WHERE plus_one = 1")
    plus_ones = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "present": present,
        "paid": paid,
        "unpaid": unpaid,
        "plus_ones": plus_ones
    }