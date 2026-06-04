from database.formaly_database_manager import init_db
import tkinter as tk
from pages.support.support_dashboard import SupportDashboard


def main():
    # 1. Ensure database exists and tables are ready
    init_db()

    # 2. Launch support dashboard (temporary)
    root = tk.Tk()
    root.title("Support Dashboard - Formaly")

    page = SupportDashboard(root, controller=None)
    page.pack(fill="both", expand=True)

    root.geometry("900x700")
    root.mainloop()


if __name__ == "__main__":
    main()