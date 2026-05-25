from database.formaly_database_manager import init_db
from pages.login.formaly_login import FormalyLoginApp


def main():
    # 1. Ensure database exists and tables are ready
    init_db()

    # 2. Launch login screen
    app = FormalyLoginApp()
    app.mainloop()


if __name__ == "__main__":
    main()