import sqlite3

DB_PATH = "database/formaly.db"

# ---------------- CONNECTION ----------------
def connect():
    return sqlite3.connect(DB_PATH)


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

    con.commit()
    con.close()


# ---------------- ACCOUNTS ----------------
def get_user(username, password_hash, role):
    con = connect()
    cur = con.cursor()

    cur.execute("""
        SELECT * FROM Accounts
        WHERE LOWER(Username)=LOWER(?)
        AND Password_Hashed=?
        AND Role=?
    """, (username, password_hash, role))

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