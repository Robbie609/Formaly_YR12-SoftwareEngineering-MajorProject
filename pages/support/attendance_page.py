import tkinter as tk
from tkinter import ttk
from database.formaly_database_manager import get_all_attendees, update_attendance, update_plus_one
from utils.styles import (
    BG, CARD, ENTRY, BORDER, GOLD, GOLD_HOV,
    TEXT_LIGHT, TEXT_MUTED, ERROR, SUCCESS,
    FONT_BODY, FONT_BOLD, FONT_H3, FONT_SMALL,
)
from utils.widgets import build_subpage_header, navigate


class AttendancePage(tk.Frame):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, bg=BG)
        self.parent   = parent
        self.user     = user
        self._imgs    = []
        self._selected = None
        self._build()

    def _back(self):
        navigate(self, self.parent, "support", self.user)

    def _build(self):

        build_subpage_header(self, "ATTENDANCE", self._back, self._imgs)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=18)

        # Search bar
        search_frame = tk.Frame(body, bg=CARD, bd=1, relief="solid")
        search_frame.pack(fill="x", pady=(0, 14), padx=4, ipady=4)
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh())
        tk.Entry(search_frame, textvariable=self._search_var,
                 bg=CARD, fg=TEXT_MUTED, font=FONT_BODY,
                 relief="flat", insertbackground=TEXT_LIGHT,
                 width=40).pack(side="left", padx=8, pady=4)
        tk.Label(search_frame, text="🔍", bg=CARD, fg=TEXT_MUTED,
                 font=("Segoe UI Emoji", 14)).pack(side="right", padx=8)

        # Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("A.Treeview",
                        background=CARD, foreground=TEXT_LIGHT,
                        fieldbackground=CARD, rowheight=38, font=FONT_BODY,
                        borderwidth=1, relief="solid")
        style.configure("A.Treeview.Heading",
                        background=ENTRY, foreground=TEXT_LIGHT,
                        font=FONT_BOLD, relief="flat")
        style.map("A.Treeview",
                  background=[("selected", GOLD)],
                  foreground=[("selected", CARD)])

        cols = ("name", "plus_one", "paid", "present")
        self._tree = ttk.Treeview(body, columns=cols, show="headings",
                                  style="A.Treeview")
        for col, heading, width in [
            ("name",     "Student Name", 340),
            ("plus_one", "Plus One",     180),
            ("paid",     "Paid",         180),
            ("present",  "Present",      180),
        ]:
            self._tree.heading(col, text=heading)
            self._tree.column(col, anchor="center", width=width)
        self._tree.column("name", anchor="w")
        self._tree.pack(fill="both", expand=True)
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        # Action buttons
        act = tk.Frame(body, bg=BG)
        act.pack(anchor="e", pady=(14, 0))

        self._btn_plus    = self._action_btn(act, "Mark Plus One",  GOLD,    lambda: self._toggle_plus(1))
        self._btn_present = self._action_btn(act, "Mark Present",   SUCCESS, lambda: self._toggle_present(1))

        self._refresh()

    def _action_btn(self, parent, text, bg, cmd):
        btn = tk.Button(parent, text=text, bg=bg, fg=CARD,
                        font=FONT_BOLD, relief="flat", cursor="hand2",
                        padx=18, pady=10, command=cmd,
                        activebackground=GOLD_HOV, state="disabled")
        btn.pack(side="left", padx=(0, 12))
        return btn

    def _refresh(self):
        query = self._search_var.get().strip() if hasattr(self, "_search_var") else ""
        for row in self._tree.get_children():
            self._tree.delete(row)
        self._selected = None
        self._set_btns(False)

        attendees = get_all_attendees(query)
        for a in attendees:
            plus_v    = "Yes" if a["plus_one"] else "No"
            paid_v    = "Yes" if a["paid"]     else "No"
            present_v = "✔"  if a["attendance"] else "✘"
            self._tree.insert("", "end", iid=str(a["id"]),
                              values=(a["name"], plus_v, paid_v, present_v))

    def _on_select(self, _event=None):
        sel = self._tree.focus()
        if sel:
            self._selected = sel
            self._set_btns(True)

    def _set_btns(self, enabled):
        state = "normal" if enabled else "disabled"
        self._btn_plus.config(state=state)
        self._btn_present.config(state=state)

    def _toggle_present(self, val):
        if not self._selected: return
        update_attendance(int(self._selected), val)
        self._refresh()

    def _toggle_plus(self, val):
        if not self._selected: return
        update_plus_one(int(self._selected), val)
        self._refresh()