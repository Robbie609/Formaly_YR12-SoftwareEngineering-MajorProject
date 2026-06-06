import tkinter as tk
import sqlite3
from datetime import datetime

from utils.styles import (
    BG, CARD, PRIMARY, SECONDARY, SUCCESS, ERROR, BORDER, 
    FONT, FONT_BOLD, TITLE, SUBTITLE, SMALL, PADDING_X, PADDING_Y
)
from utils.helpers import *

class AdminDashboard(tk.Frame):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, bg=BG)
        self.parent = parent
        self.controller = controller
        self.user = user

        self.stats = {
            'total_attendees': 0, 'checked_in': 0, 
            'total_tasks': 0, 'completed_tasks': 0, 'total_venues': 0
        }
        self.recent_tasks = []

        self._load_statistics()
        self._setup_layout()

    def _load_statistics(self):
        try:
            with sqlite3.connect("database/formaly.db") as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM attendees")
                self.stats["total_attendees"] = cursor.fetchone()

                cursor.execute("SELECT COUNT(*) FROM attendees WHERE attendance = 1")
                self.stats["checked_in"] = cursor.fetchone()

                cursor.execute("SELECT COUNT(*) FROM tasks")
                self.stats["total_tasks"] = cursor.fetchone()

                cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
                self.stats["completed_tasks"] = cursor.fetchone()

                cursor.execute("SELECT COUNT(*) FROM venues")
                self.stats["total_venues"] = cursor.fetchone()

                cursor.execute("""
                    SELECT title, priority, status, due_date
                    FROM tasks
                    ORDER BY due_date ASC
                    LIMIT 5
                """)
                self.recent_tasks = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Database Error: {e}")

    def _setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self._render_sidebar()
        
        self.content_frame = tk.Frame(self, bg=BG)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=PADDING_X, pady=PADDING_Y)
        
        self._render_header()
        self._render_metrics()
        self._render_activity()

    def _render_sidebar(self):
        sidebar = tk.Frame(self, bg=CARD, width=260)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        
        tk.Label(sidebar, text="Formaly.", font=TITLE, bg=CARD, fg=PRIMARY, anchor="w").pack(fill="x", padx=PADDING_X, pady=(PADDING_Y, PADDING_Y * 2))
        
        nav_items = [
            ("Dashboard", "dashboard", True),
            ("Tasks", "tasks", False),
            ("Venue", "venue", False),
            ("Attendance", "attendance", False),
            ("Reports", "reports", False)
        ]
        
        for text, target, is_active in nav_items:
            self._create_nav_button(sidebar, text, target, is_active)

        logout_frame = tk.Frame(sidebar, bg=CARD)
        logout_frame.pack(side="bottom", fill="x", pady=PADDING_Y)
        lbl = tk.Label(logout_frame, text="Logout", font=FONT_BOLD, bg=CARD, fg=ERROR, anchor="w", cursor="hand2")
        lbl.pack(fill="x", padx=PADDING_X, pady=8)
        lbl.bind("<Button-1>", lambda e: self.navigate("logout"))

    def _create_nav_button(self, parent, text, target, is_active):
        bg_color = BORDER if is_active else CARD
        fg_color = PRIMARY if is_active else SECONDARY
        
        btn_frame = tk.Frame(parent, bg=bg_color)
        btn_frame.pack(fill="x", pady=2)
        
        if is_active:
            tk.Frame(btn_frame, bg=PRIMARY, width=4).pack(side="left", fill="y")
        
        lbl = tk.Label(btn_frame, text=text, font=FONT_BOLD, bg=bg_color, fg=fg_color, anchor="w", cursor="hand2")
        lbl.pack(side="left", fill="both", expand=True, padx=20, pady=12)
        
        if not is_active:
            lbl.bind("<Button-1>", lambda e, t=target: self.navigate(t))

    def _render_header(self):
        header_frame = tk.Frame(self.content_frame, bg=BG)
        header_frame.pack(fill="x", pady=(0, PADDING_Y))
        
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        tk.Label(header_frame, text="Admin Dashboard", font=TITLE, bg=BG, fg=PRIMARY, anchor="w").pack(fill="x")
        tk.Label(header_frame, text=f"Overview • {current_date}", font=SUBTITLE, bg=BG, fg=SECONDARY, anchor="w").pack(fill="x")

    def _render_metrics(self):
        metrics_frame = tk.Frame(self.content_frame, bg=BG)
        metrics_frame.pack(fill="x", pady=(0, PADDING_Y))
        
        cards = [
            ("Total Tasks", self.stats['total_tasks']),
            ("Completed", self.stats['completed_tasks']),
            ("Checked In", f"{self.stats['checked_in']} / {self.stats['total_attendees']}"),
            ("Venues", self.stats['total_venues'])
        ]
        
        for i, (title, value) in enumerate(cards):
            metrics_frame.grid_columnconfigure(i, weight=1)
            self._create_metric_card(metrics_frame, title, value, i)

    def _create_metric_card(self, parent, title, value, col):
        card = tk.Frame(parent, bg=CARD, padx=20, pady=20)
        card.grid(row=0, column=col, padx=(0, 15 if col < 3 else 0), sticky="nsew")
        
        tk.Label(card, text=title, font=SMALL, bg=CARD, fg=SECONDARY, anchor="w").pack(fill="x")
        tk.Label(card, text=str(value), font=TITLE, bg=CARD, fg=PRIMARY, anchor="w").pack(fill="x", pady=(5, 0))

    def _render_activity(self):
        activity_frame = tk.Frame(self.content_frame, bg=CARD, padx=25, pady=25)
        activity_frame.pack(fill="both", expand=True)
        
        tk.Label(activity_frame, text="Recent Tasks", font=SUBTITLE, bg=CARD, fg=PRIMARY, anchor="w").pack(fill="x", pady=(0, 15))
        
        if not self.recent_tasks:
            tk.Label(activity_frame, text="No tasks found.", font=FONT, bg=CARD, fg=SECONDARY).pack()
            return
            
        headers_frame = tk.Frame(activity_frame, bg=CARD)
        headers_frame.pack(fill="x", pady=(0, 10))
        
        for title, weight in [("Task", 3), ("Priority", 1), ("Status", 1), ("Due Date", 1)]:
            tk.Label(headers_frame, text=title, font=FONT_BOLD, bg=CARD, fg=SECONDARY, anchor="w").pack(side="left", expand=True, fill="x")
            
        tk.Frame(activity_frame, bg=BORDER, height=1).pack(fill="x", pady=(0, 10))
        
        for task in self.recent_tasks:
            row = tk.Frame(activity_frame, bg=CARD)
            row.pack(fill="x", pady=6)
            
            for i, val in enumerate(task):
                color = SUCCESS if i == 2 and val == "Completed" else PRIMARY
                tk.Label(row, text=str(val), font=FONT, bg=CARD, fg=color, anchor="w").pack(side="left", expand=True, fill="x")

    def navigate(self, target):
        self.destroy()
        
        # Elements are mounted via .place(relwidth=1, relheight=1) to prevent geometry manager clashes with root window setups
        if target == "dashboard":
            from pages.admin.admin_dashboard import AdminDashboard
            AdminDashboard(self.parent, self.controller, user=self.user).place(relwidth=1, relheight=1)
        elif target == "tasks":
            from pages.planner.task_page import TaskPage
            TaskPage(self.parent, self.controller).place(relwidth=1, relheight=1)
        elif target == "venue":
            from pages.planner.venue_page import VenueSuggestionPage
            VenueSuggestionPage(self.parent, self.controller).place(relwidth=1, relheight=1)
        elif target == "attendance":
            from pages.support.attendance_page import AttendancePage
            AttendancePage(self.parent, self.controller).place(relwidth=1, relheight=1)
        elif target == "reports":
            from pages.admin.reports_page import ReportsPage
            ReportsPage(self.parent, self.controller).place(relwidth=1, relheight=1)
        elif target == "logout":
            # If leaving the window entirely, rebuild/lift clean app instance container
            self.parent.current_user = None
            self.parent.selected_role = None
            for child in self.parent.winfo_children():
                child.destroy()
            self.parent.build_ui()