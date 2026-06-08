import tkinter as tk
from database.formaly_database_manager import *
from utils.styles import *
from utils.widgets import *

_NAV     = ["Dashboard", "Attendance"]
_NAV_MAP = {"Dashboard": "support", "Attendance": "attendance"}


class SupportDashboard(tk.Frame):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, bg=BG)
        self.parent = parent
        self.user   = user
        self._imgs  = []
        self._build()

    def _build(self):
        username = self.user["Username"] if self.user else "Support"
        att      = get_attendance_stats()
        formal   = get_formal_data()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        build_sidebar(self, _NAV, "Dashboard",
                      lambda t: navigate(self, self.parent, _NAV_MAP.get(t, t), self.user),
                      self._imgs)

        right = tk.Frame(self, bg=BG)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        build_header(right, f"Welcome, {username}", "Support Dashboard", self._imgs)

        body = tk.Frame(right, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=18)
        body.columnconfigure((0, 1, 2), weight=1)
        body.rowconfigure(1, weight=1)

        # Stat cards
        stats_row = tk.Frame(body, bg=BG)
        stats_row.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 14))
        stats_row.columnconfigure((0, 1, 2), weight=1)

        total    = att.get("total",    0)
        present  = att.get("present",  0)
        incoming = total - present

        stat_card(stats_row, "Total Attendees",   total,    0, 3)
        stat_card(stats_row, "Currently Present", present,  1, 3)
        stat_card(stats_row, "Incoming Attendees", incoming, 2, 3)

        # Event details card
        ev_card = tk.Frame(body, bg=CARD)
        ev_card.grid(row=1, column=0, columnspan=3, sticky="nsew")

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