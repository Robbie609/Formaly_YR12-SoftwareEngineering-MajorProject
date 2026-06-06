import tkinter as tk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from database.formaly_database_manager import get_attendance_stats
from utils.styles import *
from pages.support.attendance_page import AttendancePage

class SupportDashboard(tk.Frame):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True)

        # =========================
        # SIDEBAR NAVIGATION
        # =========================
        sidebar = tk.Frame(root, bg=CARD, width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo & Branding
        tk.Label(
            sidebar,
            text="FORMALY",
            bg=CARD,
            fg=PRIMARY,
            font=TITLE
        ).pack(anchor="w", padx=20, pady=(30, 5))

        tk.Label(
            sidebar,
            text="Support",
            bg=CARD,
            fg=SECONDARY,
            font=SMALL
        ).pack(anchor="w", padx=20, pady=(0, 30))

        # Navigation Buttons
        self.nav_button(sidebar, "📊 Dashboard", lambda: self.controller.show_frame(SupportDashboard) if self.controller else None)
        self.nav_button(sidebar, "👥 Attendance", lambda: self.controller.show_frame(AttendancePage) if self.controller else None)

        # Spacer
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=15, pady=20)

        # Logout
        self.nav_button(sidebar, "Logout", self.logout, danger=True)

        # =========================
        # MAIN CONTENT AREA
        # =========================
        main = tk.Frame(root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        # Header Section
        header = tk.Frame(main, bg=BG)
        header.pack(fill="x", padx=40, pady=(35, 10))

        tk.Label(
            header,
            text="Dashboard Overview",
            bg=BG,
            fg="white",
            font=TITLE
        ).pack(anchor="w")

        # KPI Cards Container
        cards_frame = tk.Frame(main, bg=BG)
        cards_frame.pack(fill="both", expand=True, padx=40, pady=(30, 40))

        self.stat_vars = {
            "total": tk.StringVar(value="0"),
            "present": tk.StringVar(value="0"),
            "plus_ones": tk.StringVar(value="0"),
        }

        # Stats configuration: (label, key, color_accent)
        stats = [
            ("Total Attendees", "total", PRIMARY),
            ("Currently Present", "present", SUCCESS),
            ("Plus Ones", "plus_ones", PRIMARY),
        ]

        for i, (label, key, color) in enumerate(stats):
            self.create_stat_card(cards_frame, label, key, color, i)

    def create_stat_card(self, parent, label, key, color, index):
        """Create a styled stat card."""
        card = tk.Frame(
            parent,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        card.grid(row=0, column=index, padx=15, sticky="nsew", ipady=25, ipadx=30)
        parent.grid_columnconfigure(index, weight=1)

        tk.Label(
            card,
            text=label,
            bg=CARD,
            fg=SECONDARY,
            font=FONT
        ).pack(anchor="w")

        tk.Label(
            card,
            textvariable=self.stat_vars[key],
            bg=CARD,
            fg=color,
            font=("Segoe UI", 28, "bold")
        ).pack(anchor="w", pady=(12, 0))

    def nav_button(self, parent, text, command=None, danger=False):
        """Create a navigation button."""
        def on_enter(e):
            btn.config(bg=PRIMARY if not danger else ERROR, fg="black" if not danger else "white")

        def on_leave(e):
            btn.config(bg=ENTRY, fg="white")

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=ENTRY,
            fg="white",
            font=FONT,
            relief="flat",
            anchor="w",
            padx=15,
            pady=12,
            cursor="hand2",
            activebackground=PRIMARY
        )
        btn.pack(fill="x", padx=12, pady=5)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh_data()

    def refresh_data(self):
        """Refresh dashboard statistics."""
        try:
            stats = get_attendance_stats()
            self.stat_vars["total"].set(str(stats.get("total", 0)))
            self.stat_vars["present"].set(str(stats.get("present", 0)))
            self.stat_vars["plus_ones"].set(str(stats.get("plus_ones", 0)))
        except Exception as e:
            print("Error refreshing dashboard:", e)

    def logout(self):
        """Logout and return to login."""
        if self.controller and hasattr(self.controller, 'logout'):
            self.controller.logout()
