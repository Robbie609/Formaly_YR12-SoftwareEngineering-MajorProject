import sqlite3

DB_NAME = "formaly.db"

def get_connection():
    """Establish a database connection and configure it to return dictionary-like rows."""
    conn = sqlite3.connect(DB_NAME)
    # This is the crucial step: it allows the dashboard to use task['title'] instead of task
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """Initialize the database. No new data is added."""
    conn = get_connection()
    cursor = conn.cursor()
    # Safely ensure the table exists just in case, but do NOT seed any dummy data.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL,
            category TEXT,
            status TEXT NOT NULL,
            due_date TEXT,
            assigned_section TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_tasks():
    """Retrieve all existing tasks, ordering Pending tasks first, sorted by Priority."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM tasks 
        ORDER BY 
            CASE status WHEN 'Pending' THEN 1 ELSE 2 END,
            CASE priority 
                WHEN 'High' THEN 1 
                WHEN 'Medium' THEN 2 
                WHEN 'Low' THEN 3 
            END
    ''')
    rows = cursor.fetchall()
    # Convert the sqlite3.Row objects into standard Python dictionaries
    tasks = [dict(row) for row in rows]
    conn.close()
    return tasks

def add_task(title, description, priority, category, due_date, assigned_section):
    """Add a new task to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, priority, category, status, due_date, assigned_section)
        VALUES (?, ?, ?, ?, 'Pending', ?, ?)
    ''', (title, description, priority, category, due_date, assigned_section))
    conn.commit()
    conn.close()

def update_task(task_id, title, description, priority, category, due_date, assigned_section):
    """Update an existing task."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks 
        SET title=?, description=?, priority=?, category=?, due_date=?, assigned_section=? 
        WHERE task_id=?
    ''', (title, description, priority, category, due_date, assigned_section, task_id))
    conn.commit()
    conn.close()

def mark_task_complete(task_id):
    """Change a task's status to 'Completed'."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status='Completed' WHERE task_id=?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Remove a task from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_id=?", (task_id,))
    conn.commit()
    conn.close()