import tkinter as tk
from database.formaly_database_manager import *
from utils.styles import *
from utils.widgets import *

_NAV     = ["Dashboard", "Attendance"]
_NAV_MAP = {"Dashboard": "support", "Attendance": "attendance"}


class SupportDashboard(tk.Frame):
    def __init__(self, parent, controller=None, user=None, origin = None):
        super().__init__(parent, bg=BG)
        self.title("Formaly ~ Support")
        self.parent = parent
        self.user   = user
        self._imgs  = []
        self._build()
        self.origin = "support"

    def _build(self):
        username = self.user["Username"] if self.user else "Support"
        att      = get_attendance_stats()
        formal   = get_formal_data()

        build_sidebar(self, _NAV, "Dashboard",
                      lambda t: navigate(self, self.parent, _NAV_MAP.get(t, t), self.user),
                      self._imgs)

        right = tk.Frame(self, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        build_header(right, f"Welcome, {username}", "Support Dashboard", self._imgs)

        body = tk.Frame(right, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=18)

        # Stat cards
        stats_row = tk.Frame(body, bg=BG)
        stats_row.pack(fill="x", pady=(0, 14))

        total    = att.get("total",    0)
        present  = att.get("present",  0)
        incoming = total - present

        stat_card(stats_row, "Total Attendees",   total,    0, 3)
        stat_card(stats_row, "Currently Present", present,  1, 3)
        stat_card(stats_row, "Incoming Attendees", incoming, 2, 3)

        # Event details card
        ev_card = tk.Frame(body, bg=CARD)
        ev_card.pack(fill="both", expand=True)

        tk.Label(ev_card, text="EVENT DETAILS:", bg=CARD, fg=TEXT_LIGHT,
                 font=FONT_BOLD, anchor="w").pack(fill="x", padx=18, pady=(16, 10))

        rows = [
            ("Formal Name",    formal.get("formal_name") or "—"),
            ("School",         formal.get("school")       or "—"),
            ("Budget",         f"${formal.get('budget', 0):,}"  if formal.get("budget") else "—"),
            ("People Invited", str(formal.get("people_invited", 0))),
        ]
        for lbl, val in rows:
            row = tk.Frame(ev_card, bg=CARD)
            row.pack(fill="x", padx=18, pady=4)
            tk.Label(row, text=lbl + ":", bg=CARD, fg=TEXT_MUTED,
                     font=FONT_BODY, width=16, anchor="w").pack(side="left")
            tk.Label(row, text=val, bg=CARD, fg=TEXT_LIGHT,
                     font=FONT_BODY, anchor="w").pack(side="left")