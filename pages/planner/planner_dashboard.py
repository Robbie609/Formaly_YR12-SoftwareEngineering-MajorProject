import tkinter as tk
import sqlite3
from database.formaly_database_manager import get_venue_count
from utils.styles import (
    BG, CARD, BORDER, GOLD, TEXT_LIGHT, TEXT_MUTED, ERROR, SUCCESS,
    FONT_BODY, FONT_BOLD, FONT_H3, FONT_SMALL, FONT_STAT,
)
from utils.widgets import *
from utils.helpers import *

_NAV     = ["Dashboard", "Tasks", "Venues"]
_NAV_MAP = {"Dashboard": "planner", "Tasks": "tasks", "Venues": "venues"}


class PlannerDashboard(tk.Frame):
    def __init__(self, parent, controller=None, user=None, origin = None):
        super().__init__(parent, bg=BG)
        self.title("Formaly ~ Planner")
        self.parent = parent
        self.user   = user
        self._imgs  = []
        self._build()
        self.origin = "planner"

    def _build(self):
        username = self.user["Username"] if self.user else "Planner"

        build_sidebar(self, _NAV, "Dashboard",
                      lambda t: navigate(self, self.parent, _NAV_MAP.get(t, t), self.user),self._imgs)

        right = tk.Frame(self, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        build_header(right, f"Welcome, {username}", "Planner Dashboard", self._imgs)

        body = tk.Frame(right, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=18)

        # Fetch metrics
        conn   = sqlite3.connect("database/formaly.db")
        cur    = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tasks")
        total  = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM tasks WHERE status='Completed'")
        comp   = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM tasks WHERE status!='Completed'")
        pend   = cur.fetchone()[0]
        conn.close()
        venues = get_venue_count()

        # Stat cards row
        stats_row = tk.Frame(body, bg=BG)
        stats_row.pack(fill="x", pady=(0, 14))

        stat_card(stats_row, "Total Tasks",     total,  0, 4)
        stat_card(stats_row, "Completed Tasks", comp,   1, 4)
        stat_card(stats_row, "Pending Tasks",   pend,   2, 4)
        stat_card(stats_row, "Venue Options",   venues, 3, 4)

        # Lower row: upcoming tasks (left) + recent venues (right)
        lower = tk.Frame(body, bg=BG)
        lower.pack(fill="both", expand=True)

        self._upcoming_card(lower, 0)
        self._venues_card(lower, 1)

    def _upcoming_card(self, parent, col):
        card = tk.Frame(parent, bg=CARD)
        card.pack(side="left",fill="both",expand=True,padx=(0, 8) if col == 0 else (8, 0))

        tk.Label(card, text="Upcoming Tasks", bg=CARD, fg=GOLD,
                 font=FONT_H3, anchor="w").pack(fill="x", padx=18, pady=(16, 10))
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=18, pady=(0, 6))

        conn = sqlite3.connect("database/formaly.db")
        cur  = conn.cursor()
        cur.execute("SELECT title, priority, due_date FROM tasks WHERE status!='Completed' ORDER BY due_date ASC LIMIT 8")
        tasks = cur.fetchall()
        conn.close()

        if not tasks:
            tk.Label(card, text="No upcoming tasks.", bg=CARD, fg=TEXT_MUTED,
                     font=FONT_BODY).pack(padx=18, pady=20)
            return

        for title, priority, due in tasks:
            row = tk.Frame(card, bg=CARD)
            row.pack(fill="x", padx=18, pady=4)
            p_col = ERROR if priority == "High" else (GOLD if priority == "Medium" else SUCCESS)
            tk.Frame(row, bg=p_col, width=3).pack(side="left", fill="y", padx=(0, 8))
            tk.Label(row, text=truncate_text(title, 32), bg=CARD, fg=TEXT_LIGHT,
                     font=FONT_BODY, anchor="w").pack(side="left")
            tk.Label(row, text=due or "—", bg=CARD, fg=TEXT_MUTED,
                     font=FONT_SMALL, anchor="e").pack(side="right")

    def _venues_card(self, parent, col):
        card = tk.Frame(parent, bg=CARD)
        card.pack(side="left",fill="both",expand=True,padx=(8, 0) if col == 1 else (0, 8))

        tk.Label(card, text="Recent Venue Options", bg=CARD, fg=GOLD,
                 font=FONT_H3, anchor="w").pack(fill="x", padx=18, pady=(16, 10))
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=18, pady=(0, 6))

        conn = sqlite3.connect("database/formaly.db")
        cur  = conn.cursor()
        cur.execute("SELECT name, capacity, estimated_cost FROM venues ORDER BY id DESC LIMIT 8")
        venues = cur.fetchall()
        conn.close()

        if not venues:
            tk.Label(card, text="No venues listed.", bg=CARD, fg=TEXT_MUTED,
                     font=FONT_BODY).pack(padx=18, pady=20)
            return

        for name, cap, cost in venues:
            row = tk.Frame(card, bg=CARD)
            row.pack(fill="x", padx=18, pady=4)
            tk.Label(row, text=truncate_text(name, 28), bg=CARD, fg=TEXT_LIGHT,
                     font=FONT_BODY, anchor="w").pack(side="left")
            tk.Label(row, text=f"${cost:,.0f}", bg=CARD, fg=GOLD,
                     font=FONT_SMALL, anchor="e").pack(side="right")
            tk.Label(row, text=f"{cap} guests", bg=CARD, fg=TEXT_MUTED,
                     font=FONT_SMALL).pack(side="right", padx=12)