import tkinter as tk
from utils.styles import *
from utils.helpers import center_window


class AdminDashboard(tk.Tk):
    def __init__(self, user):
        super().__init__()

        self.user = user
        self.title("Formaly - Admin Dashboard")
        self.configure(bg=BG)
        self.geometry("1400x750")

        center_window(self, 1400, 750)

        self.current_page = None
        self.page_frame = None
        self.build_ui()

    def build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.build_sidebar()
        self.build_main_area()

    def build_sidebar(self):
        sidebar = tk.Frame(self, bg=CARD, width=250)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_propagate(False)
        sidebar.columnconfigure(0, weight=1)

        header = tk.Frame(sidebar, bg=PRIMARY, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="FORMALY",
            bg=PRIMARY,
            fg="black",
            font=("Segoe UI", 16, "bold")
        ).pack(expand=True)

        user_info = tk.Frame(sidebar, bg=CARD)
        user_info.pack(fill="x", padx=15, pady=15)

        tk.Label(
            user_info,
            text="Admin",
            bg=CARD,
            fg="white",
            font=FONT_BOLD
        ).pack(anchor="w")

        tk.Label(
            user_info,
            text=self.user[1] if self.user else "User",
            bg=CARD,
            fg=SECONDARY,
            font=SMALL
        ).pack(anchor="w", pady=(2, 0))

        pages = [
            ("Tasks", "task"),
            ("Approvals", "approvals"),
            ("Budget", "budget"),
            ("Reports", "reports"),
            ("Attendance", "attendance"),
            ("Venue", "venue"),
            ("Promotion", "promotion"),
            ("Guest", "guest"),
            ("Feedback", "feedback"),
        ]

        nav_frame = tk.Frame(sidebar, bg=CARD)
        nav_frame.pack(fill="both", expand=True, padx=0, pady=15)

        for label, page_id in pages:
            btn = tk.Button(
                nav_frame,
                text=label,
                bg=ENTRY,
                fg="white",
                font=FONT,
                border=0,
                cursor="hand2",
                command=lambda p=page_id: self.load_page(p),
                anchor="w",
                padx=15,
                pady=10
            )
            btn.pack(fill="x", padx=10, pady=4)
            btn.bind("<Enter>", lambda e, btn=btn: btn.config(bg=PRIMARY, fg="black"))
            btn.bind("<Leave>", lambda e, btn=btn: btn.config(bg=ENTRY, fg="white"))

        logout_btn = tk.Button(
            sidebar,
            text="Logout",
            bg=ERROR,
            fg="white",
            font=FONT_BOLD,
            border=0,
            cursor="hand2",
            command=self.logout,
            padx=15,
            pady=10
        )
        logout_btn.pack(fill="x", padx=10, pady=10)

    def build_main_area(self):
        main = tk.Frame(self, bg=BG)
        main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=1)

        header = tk.Frame(main, bg=BG)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        tk.Label(
            header,
            text="Admin Dashboard",
            bg=BG,
            fg="white",
            font=TITLE
        ).pack(anchor="w")

        self.page_frame = tk.Frame(main, bg=CARD, relief="solid", borderwidth=1)
        self.page_frame.grid(row=1, column=0, sticky="nsew")
        self.page_frame.columnconfigure(0, weight=1)
        self.page_frame.rowconfigure(0, weight=1)

    def load_page(self, page_id):
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        content = tk.Frame(self.page_frame, bg=CARD)
        content.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        page_titles = {
            "task": "Task Management",
            "approvals": "Approvals",
            "budget": "Budget",
            "reports": "Reports",
            "attendance": "Attendance",
            "venue": "Venue",
            "promotion": "Promotion",
            "guest": "Guest",
            "feedback": "Feedback"
        }

        title = page_titles.get(page_id, "Page")

        tk.Label(
            content,
            text=title,
            bg=CARD,
            fg="white",
            font=SUBTITLE
        ).pack(anchor="w", pady=(0, 15))

        tk.Label(
            content,
            text=f"{title} - Coming soon",
            bg=CARD,
            fg=SECONDARY,
            font=FONT
        ).pack(anchor="w")

    def logout(self):
        self.destroy()
        from pages.login.formaly_login import FormalyLoginApp
        app = FormalyLoginApp()
        app.mainloop()
