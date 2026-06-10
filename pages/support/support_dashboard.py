# Imports
import tkinter as tk
from database.formaly_database_manager import *
from utils.styles import *
from utils.widgets import *

#Navigation menu items
_NAV     = ["Dashboard", "Attendance"]
_NAV_MAP = {"Dashboard": "support", "Attendance": "attendance"}

# Class for the Support Dashboard
class SupportDashboard(tk.Frame):
    # Initialising the support dashboard
    def __init__(self, parent, controller=None, user=None, origin = None):
        super().__init__(parent, bg=BG)
        self.parent = parent
        self.user   = user
        self._imgs  = []
        self._build()
        self.origin = "support"
    # Creating the dashboard layout
    def _build(self):
        # Retrieving the current user information
        username = self.user["Username"] if self.user else "Support"
        #Retrieving attendance stats
        att      = get_attendance_stats()
        #Retrieving formal event invitation
        formal   = get_formal_data()
        #Creating the sidebar navigation menu
        build_sidebar(self, _NAV, "Dashboard",
                      lambda t: navigate(self, self.parent, _NAV_MAP.get(t, t), self.user),
                      self._imgs)
        # Creating the main content area
        right = tk.Frame(self, bg=BG)
        right.pack(side="right", fill="both", expand=True)
        # Creating the dashboard header
        build_header(right, f"Welcome, {username}", "Support Dashboard", self._imgs)
        # Creating the dashboard body
        body = tk.Frame(right, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=18)

        # Creating the statistics cards section
        stats_row = tk.Frame(body, bg=BG)
        stats_row.pack(fill="x", pady=(0, 14))
        # Calculating the attendance stastics 
        total    = att.get("total",    0)
        present  = att.get("present",  0)
        incoming = total - present
        # Creating the statistics cards
        stat_card(stats_row, "Total Attendees",   total,    0, 3)
        stat_card(stats_row, "Currently Present", present,  1, 3)
        stat_card(stats_row, "Incoming Attendees", incoming, 2, 3)

        # Creating the event details card
        ev_card = tk.Frame(body, bg=CARD)
        ev_card.pack(fill="both", expand=True)
        # Creating the event details heading
        tk.Label(ev_card, text="EVENT DETAILS:", bg=CARD, fg=TEXT_LIGHT,
                 font=FONT_BOLD, anchor="w").pack(fill="x", padx=18, pady=(16, 10))

        # Creating the event details data
        rows = [
            ("Formal Name",    formal.get("formal_name") or "—"),
            ("School",         formal.get("school")       or "—"),
            ("Budget",         f"${formal.get('budget', 0):,}"  if formal.get("budget") else "—"),
            ("People Invited", str(formal.get("people_invited", 0))),
        ]
        # Creating the event details rows
        for lbl, val in rows:
            row = tk.Frame(ev_card, bg=CARD)
            row.pack(fill="x", padx=18, pady=4)
            tk.Label(row, text=lbl + ":", bg=CARD, fg=TEXT_MUTED,
                     font=FONT_BODY, width=16, anchor="w").pack(side="left")
            tk.Label(row, text=val, bg=CARD, fg=TEXT_LIGHT,
                     font=FONT_BODY, anchor="w").pack(side="left")