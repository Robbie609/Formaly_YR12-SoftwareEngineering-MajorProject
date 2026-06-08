import tkinter as tk
from database.formaly_database_manager import get_formal_data
from utils.styles import (
    BG, CARD, BORDER, GOLD, TEXT_LIGHT, TEXT_MUTED,
    FONT_BODY, FONT_BOLD, FONT_H2, FONT_H3, FONT_SMALL, FONT_STAT, ENTRY,
)
from utils.widgets import build_sidebar, build_header, navigate

_NAV     = ["Dashboard", "Tasks", "Venues", "Attendance", "Reports"]
_NAV_MAP = {"Dashboard": "admin", "Tasks": "tasks", "Venues": "venues",
            "Attendance": "attendance", "Reports": "reports"}


class ReportsPage(tk.Frame):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, bg=BG)
        self.parent = parent
        self.user   = user
        self._imgs  = []
        self._build()

    def _build(self):
        formal = get_formal_data()

        build_sidebar(self, _NAV, "Reports",
                      lambda t: navigate(self, self.parent, _NAV_MAP.get(t, t), self.user),
                      self._imgs)

        right = tk.Frame(self, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        # Header: "Formal Report" — "Formal" gold, "Report" white
        bar = tk.Frame(right, bg="#0B0B0B", height=130)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        from utils.widgets import HDR_BG
        mid = tk.Frame(bar, bg=HDR_BG)
        mid.pack(side="left", padx=24, expand=True, fill="both")
        title_row = tk.Frame(mid, bg=HDR_BG)
        title_row.pack(anchor="w", pady=(28, 0))
        tk.Label(title_row, text="Formal ", bg=HDR_BG, fg=GOLD,       font=FONT_H2).pack(side="left")
        tk.Label(title_row, text="Report",  bg=HDR_BG, fg=TEXT_LIGHT, font=FONT_H2).pack(side="left")
        icons = tk.Frame(bar, bg=HDR_BG)
        icons.pack(side="right", padx=24)
        tk.Label(icons, text="🔔", bg=HDR_BG, fg=TEXT_LIGHT, font=("Segoe UI Emoji", 18)).pack(side="left", padx=6)
        tk.Label(icons, text="👤", bg=HDR_BG, fg=GOLD,       font=("Segoe UI Emoji", 22)).pack(side="left", padx=6)

        # Main report card
        body = tk.Frame(right, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=18)

        card = tk.Frame(body, bg=CARD)
        card.pack(side="left", fill="both", expand=True)

        formal_name = formal.get("formal_name") or "Formal"
        tk.Label(card, text=f"{formal_name} Report", bg=CARD, fg=GOLD,
                 font=FONT_H3, anchor="center").pack(fill="x", pady=(20, 6))
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(0, 16))

        rows = [
            ("People that were invited:",            formal.get("people_invited",  0)),
            ("People that attended:",                formal.get("people_attended", 0)),
            ("Budget Set:",                          f"${formal.get('budget',    0):,}"),
            ("Total Expenses:",                      f"${formal.get('expenses',  0):,}"),
            ("Number of Issues that occured:",       formal.get("issues_occured",   0)),
            ("Number of Issues that were resolved:", formal.get("issues_resolved",  0)),
        ]

        for label, value in rows:
            row = tk.Frame(card, bg=CARD)
            row.pack(fill="x", padx=32, pady=8)
            tk.Label(row, text=label, bg=CARD, fg=GOLD,
                     font=FONT_BOLD, anchor="w").pack(side="left")
            tk.Label(row, text=str(value), bg=CARD, fg=GOLD,
                     font=FONT_STAT, anchor="e").pack(side="right")

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(8, 6))

        feedback_label = formal.get("feedback") or "No feedback recorded."
        tk.Label(card, text="Feedback from guests:", bg=CARD, fg=GOLD,
                 font=FONT_BOLD, anchor="w").pack(fill="x", padx=32, pady=(8, 4))

        fb_row = tk.Frame(card, bg=CARD)
        fb_row.pack(fill="x", padx=32, pady=(0, 20))
        fb_row.columnconfigure((0, 1), weight=1)

        fb1 = tk.Frame(fb_row, bg=ENTRY, height=80)
        fb1.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(fb1, text=str(feedback_label), bg=ENTRY, fg=TEXT_MUTED,
                 font=FONT_BODY, wraplength=280,
                 justify="left").pack(padx=8, pady=8, anchor="w")

        fb2 = tk.Frame(fb_row, bg=ENTRY, height=80)
        fb2.pack(side="left", fill="x", expand=True, padx=(8, 0))