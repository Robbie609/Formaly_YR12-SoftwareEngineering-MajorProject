from database.formaly_database_manager import init_db
import tkinter as tk
from pages.login.formaly_login import FormalyLoginApp


def main():
    # Initialize database
    init_db()
    
    # Launch login page as entry point
    app = FormalyLoginApp()
    app.mainloop()


if __name__ == "__main__":
    main()
