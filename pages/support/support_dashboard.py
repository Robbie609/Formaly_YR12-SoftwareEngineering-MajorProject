import tkinter as tk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from database.formaly_database_manager import get_attendance_stats
from utils.styles import *


class SupportDashboard(tk.Frame):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.user = user
        self.setup_ui()

    # =========================
    # UI
    # =========================
    def setup_ui(self):

        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True)

        # =========================
        # SIDEBAR (ROLE SAFE)
        # =========================
        sidebar = tk.Frame(root, bg=CARD, width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="FORMALY",
            bg=CARD,
            fg=PRIMARY,
            font=TITLE
        ).pack(anchor="w", padx=20, pady=(25, 5))

        tk.Label(
            sidebar,
            text="Support Panel",
            bg=CARD,
            fg=SECONDARY,
            font=SMALL
        ).pack(anchor="w", padx=20, pady=(0, 25))

        # --- NAV SAFE (SUPPORT ONLY) ---
        self.nav_button(sidebar, "Dashboard")
        self.nav_button(sidebar, "Attendance", self.open_attendance)

        # ❌ intentionally NOT included:
        # Reports, Settings (role restriction fix)

        # =========================
        # LOGOUT (IMPORTANT FIX)
        # =========================
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=15, pady=15)

        self.nav_button(sidebar, "Logout", self.logout, danger=True)

        # =========================
        # MAIN AREA
        # =========================
        main = tk.Frame(root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        content = tk.Frame(main, bg=BG)
        content.pack(fill="both", expand=True, padx=30, pady=25)

        # =========================
        # HEADER
        # =========================
        tk.Label(
            content,
            text="Support Dashboard",
            bg=BG,
            fg="white",
            font=TITLE
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Live attendance overview and system status",
            bg=BG,
            fg=SECONDARY,
            font=FONT
        ).pack(anchor="w", pady=(4, 20))

        # =========================
        # KPI CARDS (FIXED VISIBILITY)
        # =========================
        self.stats_frame = tk.Frame(content, bg=BG)
        self.stats_frame.pack(fill="x", pady=(0, 25))

        self.stat_vars = {
            "total": tk.StringVar(value="0"),
            "present": tk.StringVar(value="0"),
            "paid": tk.StringVar(value="0"),
            "unpaid": tk.StringVar(value="0"),
            "plus_ones": tk.StringVar(value="0"),
        }

        stats = [
            ("Total Attendees", "total"),
            ("Present", "present"),
            ("Paid", "paid"),
            ("Unpaid", "unpaid"),
            ("Plus Ones", "plus_ones")
        ]

        for i, (label, key) in enumerate(stats):
            card = tk.Frame(
                self.stats_frame,
                bg=CARD,
                padx=18,
                pady=15,
                highlightthickness=1,
                highlightbackground=BORDER
            )
            card.grid(row=0, column=i, padx=10, sticky="nsew")

            tk.Label(
                card,
                text=label,
                bg=CARD,
                fg=SECONDARY,
                font=SMALL
            ).pack(anchor="w")

            # 🔥 BIG NUMBER FIX (was missing / unclear before)
            tk.Label(
                card,
                textvariable=self.stat_vars[key],
                bg=CARD,
                fg=PRIMARY,
                font=("Segoe UI", 22, "bold")
            ).pack(anchor="w", pady=(8, 0))

            self.stats_frame.grid_columnconfigure(i, weight=1)

        # =========================
        # ACTION PANEL
        # =========================
        action = tk.Frame(
            content,
            bg=CARD,
            padx=20,
            pady=18,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        action.pack(fill="x")

        tk.Label(
            action,
            text="Quick Action",
            bg=CARD,
            fg="white",
            font=FONT_BOLD
        ).pack(anchor="w")

        tk.Label(
            action,
            text="Manage attendance records and updates",
            bg=CARD,
            fg=SECONDARY,
            font=SMALL
        ).pack(anchor="w", pady=(3, 10))

        btn = tk.Button(
            action,
            text="Open Attendance Manager →",
            command=self.open_attendance,
            bg=PRIMARY,
            fg="black",
            font=FONT_BOLD,
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            activebackground="#FFE27A"
        )
        btn.pack(anchor="w")

        btn.bind("<Enter>", lambda e: btn.config(bg="#FFE27A"))
        btn.bind("<Leave>", lambda e: btn.config(bg=PRIMARY))

    # =========================
    # NAV BUTTON FACTORY
    # =========================
    def nav_button(self, parent, text, command=None, danger=False):

        def on_enter(e):
            btn.config(bg=PRIMARY if not danger else ERROR, fg="black")

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
            pady=10,
            cursor="hand2",
            activebackground=PRIMARY
        )

        btn.pack(fill="x", padx=15, pady=5)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    # =========================
    # NAVIGATION
    # =========================
    def open_attendance(self):
        if self.controller and hasattr(self.controller, "show_frame"):
            self.controller.show_frame("AttendancePage")

    def logout(self):
        if self.controller:
            try:
                self.controller.destroy()
            except:
                pass

    # =========================
    # DATA REFRESH
    # =========================
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh_data()

    def refresh_data(self):
        try:
            stats = get_attendance_stats()

            self.stat_vars["total"].set(stats.get("total", 0))
            self.stat_vars["present"].set(stats.get("present", 0))
            self.stat_vars["paid"].set(stats.get("paid", 0))
            self.stat_vars["unpaid"].set(stats.get("unpaid", 0))
            self.stat_vars["plus_ones"].set(stats.get("plus_ones", 0))

        except Exception as e:
            print("Dashboard load error:", e)