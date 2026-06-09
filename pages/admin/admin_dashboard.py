import tkinter as tk
from tkinter import messagebox
from database.formaly_database_manager import (
    get_formal_data, get_pending_task_count, get_attendance_stats,
    get_venue_count, update_formal_data,
)
from utils.styles import (
    BG, CARD, ENTRY, BORDER, GOLD, GOLD_HOV,
    TEXT_LIGHT, TEXT_MUTED, ERROR, SUCCESS,
    FONT_BODY, FONT_BOLD, FONT_H2, FONT_H3, FONT_SMALL, FONT_STAT,
)
from utils.widgets import build_sidebar, build_header, stat_card, navigate, make_modal, modal_field
from pages.attendee.attendee_dashboard import FormalInvitationPage


_NAV     = ["Dashboard", "Tasks", "Venues", "Attendance", "Reports"]
_NAV_MAP = {"Dashboard": "admin", "Tasks": "tasks", "Venues": "venues",
            "Attendance": "attendance", "Reports": "reports", "Attendee" : "attendee"}


class AdminDashboard(tk.Frame):
    def __init__(self, parent, controller=None, user=None, origin=None):
        super().__init__(parent, bg=BG)
        self.title("Formaly ~ Admin")
        self.parent = parent
        self.user   = user
        self._imgs  = []
        self._build()
        self.origin = "admin"

    def _build(self):
        username = self.user["Username"] if self.user else "Admin"
        formal   = get_formal_data()

        build_sidebar(self,_NAV,"Dashboard",lambda t: navigate(self, self.parent, _NAV_MAP.get(t, t), self.user),self._imgs)

        right = tk.Frame(self, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        build_header(right, f"Welcome, {username}", "Admin Dashboard", self._imgs)

        body = tk.Frame(right, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=18)

        # Stat cards
        stats_row = tk.Frame(body, bg=BG)
        stats_row.pack(fill="x", pady=(0, 14))

        pending = get_pending_task_count()
        att     = get_attendance_stats()
        venues  = get_venue_count()

        stat_card(stats_row, "Tasks Pending",   pending,             0, 3)
        stat_card(stats_row, "Venue Selected",  venues,              1, 3)
        stat_card(stats_row, "Total Attendees", att.get("total", 0), 2, 3)

        # Lower row: event details (left 2/3) + budget (right 1/3)
        ev_card = tk.Frame(body, bg=CARD)
        ev_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(ev_card, text="EVENT DETAILS:", bg=CARD, fg=TEXT_LIGHT,
                 font=FONT_BOLD, anchor="w").pack(fill="x", padx=18, pady=(16, 8))

        ev_name = formal.get("formal_name") or "—"
        ev_date = formal.get("budget")       or "—"
        fid     = formal.get("formal_id")

        self._detail_row(ev_card, "Name:", ev_name,
                         lambda: self._edit(fid, "formal_name", ev_name))
        tk.Frame(ev_card, bg=BORDER, height=1).pack(fill="x", padx=18)
        self._detail_row(ev_card, "Date:", "TBA", lambda: None)

        sub_btn = tk.Button(ev_card, text="Submit Invitation",
                            bg=GOLD, fg=TEXT_LIGHT, font=FONT_BOLD,
                            relief="flat", cursor="hand2",
                            activebackground=GOLD_HOV, activeforeground=TEXT_LIGHT,
                            command=lambda: navigate(self, self.parent, "invitation", self.user))
        sub_btn.pack(anchor="w", padx=18, pady=14)
        sub_btn.bind("<Enter>", lambda e: sub_btn.config(bg=GOLD_HOV))
        sub_btn.bind("<Leave>", lambda e: sub_btn.config(bg=GOLD))

        # Budget card
        bud_card = tk.Frame(body, bg=CARD)
        bud_card.pack(side="right", fill="both", expand=True)

        tk.Label(bud_card, text="Budget", bg=CARD, fg=TEXT_LIGHT,
                 font=FONT_BOLD, anchor="w").pack(fill="x", padx=18, pady=(16, 6))

        budget  = formal.get("budget",   0) or 0
        expenses = formal.get("expenses", 0) or 0
        pct = max(0.0, min(1.0, expenses / budget)) if budget else 0.0

        tk.Label(bud_card, text=f"${budget:,}", bg=CARD, fg=GOLD,
                 font=FONT_H3).pack(anchor="w", padx=18)

        bar_bg = tk.Frame(bud_card, bg=BORDER, height=12)
        bar_bg.pack(fill="x", padx=18, pady=12)

        fill = tk.Frame(bar_bg, bg=GOLD, height=12)
        fill.place(relx=0, rely=0, relwidth=pct, relheight=1)

        edit_bud = tk.Button(bud_card, text="Edit", bg=ENTRY, fg=TEXT_LIGHT,
                             font=FONT_SMALL, relief="flat", cursor="hand2",
                             activebackground=BORDER,
                             command=lambda: self._edit(fid, "budget", budget))
        edit_bud.pack(anchor="w", padx=18, pady=(0, 14))

    def _detail_row(self, parent, label, value, edit_cmd):
        row = tk.Frame(parent, bg=CARD)
        row.pack(fill="x", padx=18, pady=8)
        tk.Label(row, text=label, bg=CARD, fg=TEXT_LIGHT,
                 font=FONT_BOLD, width=7, anchor="w").pack(side="left")
        tk.Label(row, text=str(value), bg=CARD, fg=TEXT_MUTED,
                 font=FONT_BODY, anchor="w").pack(side="left", expand=True, fill="x")
        btn = tk.Button(row, text="Edit", bg=ENTRY, fg=TEXT_LIGHT,
                        font=FONT_SMALL, relief="flat", cursor="hand2",
                        command=edit_cmd, activebackground=BORDER)
        btn.pack(side="right")

    def _edit(self, fid, field, current):
        if not fid:
            messagebox.showinfo("Notice", "No formal data record found.")
            return
        m = make_modal(self, f"Edit {field}", 360, 160)
        f = tk.Frame(m, bg=m.cget("bg"), padx=20, pady=20)
        f.pack(fill="both", expand=True)
        ent = modal_field(f, field.replace("_", " ").title(), str(current))
        def _save():
            val = ent.get().strip()
            try:
                val = int(val) if field in ("budget", "expenses") else val
            except ValueError:
                pass
            update_formal_data(fid, **{field: val})
            m.destroy()
            navigate(self, self.parent, "admin", self.user)
        tk.Button(f, text="Save", bg=GOLD, fg=TEXT_LIGHT, font=FONT_BOLD,
                  relief="flat", cursor="hand2",
                  activebackground=GOLD_HOV, command=_save).pack(anchor="e", pady=(10, 0))