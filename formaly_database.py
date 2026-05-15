import sqlite3

def create_accounts_table():
    # Connect to the database file
    conn = sqlite3.connect('formal.db')
    cursor = conn.cursor()

    # Define the accounts table schema
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        school TEXT NOT NULL,
        formal_name TEXT,
        role TEXT NOT NULL CHECK (role IN ('admin', 'planner', 'helper'))
    );
    """

    try:
        # Execute and save changes
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table 'accounts' created successfully in formal.db")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close connection
        conn.close()

if __name__ == '__main__':
    create_accounts_table()