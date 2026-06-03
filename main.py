from database.formaly_database_manager import init_db
import tkinter as tk
from pages.attendee.feedback_page import FormalFeedbackPage


def main():
    # 1. Ensure database exists and tables are ready
    init_db()

    # 2. Launch feedback page (temporary)
    root = tk.Tk()
    root.title("Formal Feedback - Formaly")

    page = FormalFeedbackPage(root, controller=None)
    page.pack(fill="both", expand=True)

    root.geometry("900x700")
    root.mainloop()


if __name__ == "__main__":
    main()