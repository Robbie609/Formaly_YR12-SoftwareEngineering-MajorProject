import sqlite3
import os

DB_PATH = os.path.join("database", "formaly.db")

def drop_new_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("DROP TABLE IF EXISTS accounts_new")
        conn.commit()
        print("accounts_new table deleted successfully.")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error deleting table: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    drop_new_table()