# pages/planner/planner_dashboard.py

import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
import os

from utils.styles import (
    BG, CARD, ENTRY, PRIMARY, SECONDARY, SUCCESS, ERROR, BORDER,
    FONT, FONT_BOLD, TITLE, SUBTITLE, SMALL, PADDING_X, PADDING_Y
)
from utils.helpers import clear_frame, format_date, truncate_text

class PlannerDashboard(tk.Frame):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, bg=BG)

        self.parent = parent
        self.controller = controller
        self.user = user

        self.init_database()
        self.setup_layout()
        
    def init_database(self):
        os.makedirs("database", exist_ok=True)
        conn = sqlite3.connect("database/formaly.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM venues")
        conn.commit()
        conn.close()

    def setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar Panel
        self.sidebar = tk.Frame(self, bg=CARD, width=260, bd=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Main Layout Workspace
        self.main_content = tk.Frame(self, bg=BG)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=PADDING_X, pady=PADDING_Y)
        self.main_content.grid_rowconfigure(2, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        self.render_sidebar("Dashboard")
        self.render_dashboard_content()

    def render_sidebar(self, active_page):
        # Brand Header
        brand_frame = tk.Frame(self.sidebar, bg=CARD, pady=24)
        brand_frame.pack(fill="x", padx=24)
        brand_label = tk.Label(brand_frame, text="Formaly", font=TITLE, fg=PRIMARY, bg=CARD)
        brand_label.pack(anchor="w")
        
        sep = tk.Frame(self.sidebar, bg=BORDER, height=1)
        sep.pack(fill="x", padx=16, pady=(0, 24))

        # Navigation Options
        menu_items = [
            ("Dashboard", "Dashboard"),
            ("Tasks", "Tasks"),
            ("Venue Suggestions", "Venues"),
        ]

        for display_name, internal_name in menu_items:
            is_active = (display_name == active_page)
            btn_bg = BG if is_active else CARD
            btn_fg = PRIMARY if is_active else SECONDARY
            
            btn_frame = tk.Frame(self.sidebar, bg=btn_bg, height=44)
            btn_frame.pack(fill="x", padx=16, pady=4)
            btn_frame.pack_propagate(False)
            
            if is_active:
                indicator = tk.Frame(btn_frame, bg=PRIMARY, width=4)
                indicator.pack(side="left", fill="y")

            btn = tk.Button(
                btn_frame,
                text=f"  {display_name}",
                font=FONT_BOLD if is_active else FONT,
                fg=btn_fg,
                bg=btn_bg,
                activebackground=BG,
                activeforeground=PRIMARY,
                bd=0,
                relief="flat",
                anchor="w",
                command=lambda dest=display_name: self.navigate_to(dest)
            )
            btn.pack(side="left", fill="both", expand=True, padx=(8 if not is_active else 4, 0))

        # Footer Actions
        logout_frame = tk.Frame(self.sidebar, bg=CARD, height=60)
        logout_frame.pack(side="bottom", fill="x", padx=16, pady=16)
        logout_frame.pack_propagate(False)
        
        logout_btn = tk.Button(
            logout_frame,
            text="Log Out",
            font=FONT_BOLD,
            fg=ERROR,
            bg=CARD,
            activebackground=BG,
            activeforeground=ERROR,
            bd=0,
            relief="flat",
            anchor="w",
        )
        logout_btn.pack(fill="both", expand=True, padx=8)

    def navigate_to(self, page_name):
        if page_name == "Dashboard":
            return

    # Remove current page
        self.destroy()

        if page_name == "Tasks":
            from pages.planner.task_page import TaskPage

            page = TaskPage(
            self.parent,
            user=self.user)

            page.place(relwidth=1, relheight=1)
            page.lift()

        elif page_name == "Venue Suggestions":
            from pages.planner.venue_page import VenueSuggestionPage

            page = VenueSuggestionPage(
            self.parent,
            user=self.user)
            page.place(relwidth=1, relheight=1)
            page.lift()

    def fetch_metrics(self):
        conn = sqlite3.connect("database/formaly.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM tasks")
        total_tasks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
        completed_tasks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status != 'Completed'")
        pending_tasks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM venues")
        total_venues = cursor.fetchone()[0]
        
        conn.close()
        return total_tasks, completed_tasks, pending_tasks, total_venues

    def render_dashboard_content(self):
        clear_frame(self.main_content)
        
        # Header Section
        header_frame = tk.Frame(self.main_content, bg=BG)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 24))
        
        welcome_lbl = tk.Label(header_frame, text="Welcome back, Planner", font=TITLE, fg=PRIMARY, bg=BG)
        welcome_lbl.pack(anchor="w")
        
        date_str = datetime.now().strftime("%A, %B %d, %Y")
        date_lbl = tk.Label(header_frame, text=date_str, font=SMALL, fg=SECONDARY, bg=BG)
        date_lbl.pack(anchor="w", pady=(4, 0))

        # Metrics Configuration
        total_t, comp_t, pend_t, total_v = self.fetch_metrics()
        metrics = [
            ("Total Tasks", str(total_t), PRIMARY),
            ("Completed Tasks", str(comp_t), SUCCESS),
            ("Pending Tasks", str(pend_t), ERROR),
            ("Venue Options", str(total_v), SECONDARY)
        ]

        metrics_panel = tk.Frame(self.main_content, bg=BG)
        metrics_panel.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 24))
        metrics_panel.grid_columnconfigure((0, 1, 2, 3), weight=1)

        for idx, (title, val, color) in enumerate(metrics):
            card_border = tk.Frame(metrics_panel, bg=BORDER, padx=1, pady=1)
            card_border.grid(row=0, column=idx, padx=8, sticky="nsew")
            
            card = tk.Frame(card_border, bg=CARD, padx=20, pady=20)
            card.pack(fill="both", expand=True)
            
            t_lbl = tk.Label(card, text=title, font=SMALL, fg=SECONDARY, bg=CARD)
            t_lbl.pack(anchor="w")
            
            v_lbl = tk.Label(card, text=val, font=TITLE, fg=color, bg=CARD)
            v_lbl.pack(anchor="w", pady=(8, 0))

        # Split Data Tables Panel
        split_panel = tk.Frame(self.main_content, bg=BG)
        split_panel.grid(row=2, column=0, columnspan=4, sticky="nsew")
        split_panel.grid_rowconfigure(0, weight=1)
        split_panel.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        self.render_upcoming_tasks_card(split_panel, 0)
        self.render_recent_venues_card(split_panel, 1)

    def render_upcoming_tasks_card(self, container, col):
        card_border = tk.Frame(container, bg=BORDER, padx=1, pady=1)
        card_border.grid(row=0, column=col, padx=8, sticky="nsew")
        
        card = tk.Frame(card_border, bg=CARD, padx=20, pady=20)
        card.pack(fill="both", expand=True)
        
        title_lbl = tk.Label(card, text="Upcoming Tasks", font=SUBTITLE, fg=PRIMARY, bg=CARD)
        title_lbl.pack(anchor="w", pady=(0, 16))

        conn = sqlite3.connect("database/formaly.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, priority, due_date FROM tasks WHERE status != 'Completed' ORDER BY due_date ASC LIMIT 5")
        tasks = cursor.fetchall()
        conn.close()

        if not tasks:
            empty_lbl = tk.Label(card, text="All caught up! No urgent tasks.", font=FONT, fg=SECONDARY, bg=CARD)
            empty_lbl.pack(fill="both", expand=True, pady=40)
            return

        for item, priority, due in tasks:
            item_frame = tk.Frame(card, bg=CARD, pady=8)
            item_frame.pack(fill="x")
            
            p_color = ERROR if priority == "High" else (SECONDARY if priority == "Medium" else SUCCESS)
            p_badge = tk.Label(item_frame, text=f" {priority} ", font=SMALL, fg=CARD, bg=p_color, padx=4)
            p_badge.pack(side="right")
            
            t_lbl = tk.Label(item_frame, text=truncate_text(item, 30), font=FONT_BOLD, fg=PRIMARY, bg=CARD)
            t_lbl.pack(side="left", anchor="w")
            
            d_lbl = tk.Label(item_frame, text=f"Due: {due}", font=SMALL, fg=SECONDARY, bg=CARD)
            d_lbl.pack(side="left", padx=12, anchor="w")
            
            sep = tk.Frame(card, bg=BORDER, height=1)
            sep.pack(fill="x")

    def render_recent_venues_card(self, container, col):
        card_border = tk.Frame(container, bg=BORDER, padx=1, pady=1)
        card_border.grid(row=0, column=col, padx=8, sticky="nsew")
        
        card = tk.Frame(card_border, bg=CARD, padx=20, pady=20)
        card.pack(fill="both", expand=True)
        
        title_lbl = tk.Label(card, text="Recent Venue Options", font=SUBTITLE, fg=PRIMARY, bg=CARD)
        title_lbl.pack(anchor="w", pady=(0, 16))

        conn = sqlite3.connect("database/formaly.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, capacity, estimated_cost FROM venues ORDER BY id DESC LIMIT 5")
        venues = cursor.fetchall()
        conn.close()

        if not venues:
            empty_lbl = tk.Label(card, text="No venues listed yet.", font=FONT, fg=SECONDARY, bg=CARD)
            empty_lbl.pack(fill="both", expand=True, pady=40)
            return

        for name, cap, cost in venues:
            item_frame = tk.Frame(card, bg=CARD, pady=8)
            item_frame.pack(fill="x")
            
            cost_lbl = tk.Label(item_frame, text=f"${cost:,.2f}", font=FONT_BOLD, fg=SUCCESS, bg=CARD)
            cost_lbl.pack(side="right")
            
            n_lbl = tk.Label(item_frame, text=truncate_text(name, 25), font=FONT_BOLD, fg=PRIMARY, bg=CARD)
            n_lbl.pack(side="left", anchor="w")
            
            c_lbl = tk.Label(item_frame, text=f"Cap: {cap}", font=SMALL, fg=SECONDARY, bg=CARD)
            c_lbl.pack(side="left", padx=12, anchor="w")
            
            sep = tk.Frame(card, bg=BORDER, height=1)
            sep.pack(fill="x")