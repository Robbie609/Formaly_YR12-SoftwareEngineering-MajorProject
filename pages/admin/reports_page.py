import tkinter as tk
import sqlite3
from utils.styles import (
    BG, CARD, PRIMARY, SECONDARY, SUCCESS, ERROR, BORDER,
    FONT, FONT_BOLD, TITLE, SUBTITLE, SMALL, PADDING_X, PADDING_Y
)

class ReportsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.parent = parent
        self.controller = controller
        
        self.stats = {}
        self.load_statistics()
        self.setup_layout()

    def load_statistics(self):
        # Initialize default primitive metrics safely
        self.stats = {
            "task_completion_rate": 0.0,
            "attendance_rate": 0.0,
            "total_tasks": 0,
            "completed_tasks": 0,
            "total_attendees": 0,
            "checked_in": 0
        }

        try:
            with sqlite3.connect("database/formaly.db") as conn:
                cursor = conn.cursor()

                # 1. Total Tasks
                cursor.execute("SELECT COUNT(*) FROM tasks")
                res_tasks = cursor.fetchone()
                total_tasks = int(res_tasks[0]) if (res_tasks and res_tasks is not None) else 0

                # 2. Completed Tasks
                cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
                res_comp = cursor.fetchone()
                completed_tasks = int(res_comp[0]) if (res_comp and res_comp is not None) else 0

                # 3. Total Attendees
                cursor.execute("SELECT COUNT(*) FROM attendees")
                res_att = cursor.fetchone()
                total_attendees = int(res_att[0]) if (res_att and res_att is not None) else 0

                # 4. Checked In Attendees
                cursor.execute("SELECT COUNT(*) FROM attendees WHERE attendance = 1")
                res_check = cursor.fetchone()
                checked_in = int(res_check[0]) if (res_check and res_check is not None) else 0

                # Commit cleanly assigned structural primitives back to state dictionary
                self.stats["total_tasks"] = total_tasks
                self.stats["completed_tasks"] = completed_tasks
                self.stats["total_attendees"] = total_attendees
                self.stats["checked_in"] = checked_in

                # Safe explicit float rate divisions
                if total_tasks > 0:
                    self.stats["task_completion_rate"] = (completed_tasks / total_tasks) * 100
                
                if total_attendees > 0:
                    self.stats["attendance_rate"] = (checked_in / total_attendees) * 100

        except sqlite3.Error as e:
            print(f"Database Query Error: {e}")

    def setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.render_sidebar()
        
        self.content_frame = tk.Frame(self, bg=BG)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=PADDING_X, pady=PADDING_Y)
        
        self.render_header()
        self.render_analytics_summaries()
        self.render_generation_panel()

    def render_sidebar(self):
        sidebar = tk.Frame(self, bg=CARD, width=260)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        
        tk.Label(sidebar, text="Formaly.", font=TITLE, bg=CARD, fg=PRIMARY, anchor="w").pack(fill="x", padx=PADDING_X, pady=(PADDING_Y, PADDING_Y * 2))
        
        nav_items = [
            ("Dashboard", "dashboard", False),
            ("Tasks", "tasks", False),
            ("Venue", "venue", False),
            ("Attendance", "attendance", False),
            ("Reports", "reports", True)
        ]
        
        for text, target, is_active in nav_items:
            bg_color = BORDER if is_active else CARD
            fg_color = PRIMARY if is_active else SECONDARY
            
            btn_frame = tk.Frame(sidebar, bg=bg_color)
            btn_frame.pack(fill="x", pady=2)
            
            if is_active:
                tk.Frame(btn_frame, bg=PRIMARY, width=4).pack(side="left", fill="y")
            
            lbl = tk.Label(btn_frame, text=text, font=FONT_BOLD, bg=bg_color, fg=fg_color, anchor="w", cursor="hand2")
            lbl.pack(side="left", fill="both", expand=True, padx=20, pady=12)
            
            if not is_active:
                lbl.bind("<Button-1>", lambda e, t=target: self.navigate(t))

        logout_frame = tk.Frame(sidebar, bg=CARD)
        logout_frame.pack(side="bottom", fill="x", pady=PADDING_Y)
        logout_lbl = tk.Label(logout_frame, text="Logout", font=FONT_BOLD, bg=CARD, fg=ERROR, anchor="w", cursor="hand2")
        logout_lbl.pack(fill="x", padx=PADDING_X, pady=8)
        logout_lbl.bind("<Button-1>", lambda e: self.navigate("logout"))

    def render_header(self):
        header_frame = tk.Frame(self.content_frame, bg=BG)
        header_frame.pack(fill="x", pady=(0, PADDING_Y))
        tk.Label(header_frame, text="System Reports & Analytics", font=TITLE, bg=BG, fg=PRIMARY, anchor="w").pack(fill="x")
        tk.Label(header_frame, text="Generate system exports and view high-level event statistics.", font=SUBTITLE, bg=BG, fg=SECONDARY, anchor="w").pack(fill="x")

    def render_analytics_summaries(self):
        analytics_frame = tk.Frame(self.content_frame, bg=BG)
        analytics_frame.pack(fill="x", pady=(0, PADDING_Y))
        analytics_frame.grid_columnconfigure(0, weight=1)
        analytics_frame.grid_columnconfigure(1, weight=1)

        def create_progress_card(parent, title, percentage, color, col):
            card = tk.Frame(parent, bg=CARD, padx=25, pady=25)
            card.grid(row=0, column=col, padx=(0, 15 if col == 0 else 0), sticky="nsew")
            
            tk.Label(card, text=title, font=SUBTITLE, bg=CARD, fg=PRIMARY, anchor="w").pack(fill="x", pady=(0, 15))
            tk.Label(card, text=f"{percentage:.1f}%", font=("Segoe UI", 20, "bold"), bg=CARD, fg=color, anchor="w").pack(fill="x", pady=(0, 10))
            
            canvas = tk.Canvas(card, height=8, bg=BORDER, highlightthickness=0)
            canvas.pack(fill="x")
            
            def draw_bar(event):
                canvas.delete("bar")
                width = event.width * (percentage / 100)
                canvas.create_rectangle(0, 0, width, 8, fill=color, outline=color, tags="bar")
            canvas.bind("<Configure>", draw_bar)

        create_progress_card(analytics_frame, "Task Completion Rate", self.stats['task_completion_rate'], SUCCESS, 0)
        create_progress_card(analytics_frame, "Total Attendance Rate", self.stats['attendance_rate'], PRIMARY, 1)

    def render_generation_panel(self):
        panel = tk.Frame(self.content_frame, bg=CARD, padx=30, pady=30)
        panel.pack(fill="both", expand=True)
        
        tk.Label(panel, text="Export Reports", font=SUBTITLE, bg=CARD, fg=PRIMARY, anchor="w").pack(fill="x", pady=(0, 20))
        
        btn_frame = tk.Frame(panel, bg=CARD)
        btn_frame.pack(fill="x")
        
        reports = [
            ("Generate Task Report", PRIMARY),
            ("Generate Attendance Report", SECONDARY),
            ("Generate Venue Report", BORDER)
        ]
        
        for title, color in reports:
            btn = tk.Label(btn_frame, text=title, font=FONT_BOLD, bg=color, fg="black" if color == PRIMARY else PRIMARY, padx=20, pady=10, cursor="hand2")
            btn.pack(side="left", padx=(0, 15))

    def navigate(self, target):
        self.destroy()
        
        if target == "dashboard":
            from pages.admin.admin_dashboard import AdminDashboard
            AdminDashboard(self.parent, self.controller).place(relwidth=1, relheight=1)
        elif target == "reports":
            from pages.admin.reports_page import ReportsPage
            ReportsPage(self.parent, self.controller).place(relwidth=1, relheight=1)
        elif target == "tasks":
            from pages.planner.task_page import TaskPage
            TaskPage(self.parent, self.controller).place(relwidth=1, relheight=1)
        elif target == "venue":
            from pages.planner.venue_page import VenueSuggestionPage
            VenueSuggestionPage(self.parent, self.controller).place(relwidth=1, relheight=1)
        elif target == "attendance":
            from pages.support.attendance_page import AttendancePage
            AttendancePage(self.parent, self.controller).place(relwidth=1, relheight=1)
        elif target == "logout":
            self.parent.current_user = None
            self.parent.selected_role = None
            for child in self.parent.winfo_children():
                child.destroy()
            self.parent.build_ui()