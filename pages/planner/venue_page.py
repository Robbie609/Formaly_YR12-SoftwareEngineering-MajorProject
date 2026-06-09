import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from utils.styles import (
    BG, CARD, ENTRY, BORDER, GOLD, GOLD_HOV,
    TEXT_LIGHT, TEXT_MUTED, ERROR, SUCCESS,
    FONT_BODY, FONT_BOLD, FONT_H3, FONT_SMALL,
)
from utils.widgets import build_subpage_header, scrollable_frame, make_modal, modal_field, navigate
from utils.helpers import truncate_text, clear_frame


class VenueSuggestionPage(tk.Frame):
    def __init__(self, parent, controller=None, user=None, origin=None):
        super().__init__(parent, bg=BG)
        self.parent = parent
        self.user   = user
        self._imgs  = []
        self._build()
        self.origin = origin or "planner"

    def _back(self):
        navigate(self, self.parent, self.origin, self.user)

    def _build(self):

        build_subpage_header(self, "VENUE OPTIONS", self._back, self._imgs)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        self._scroll_inner = scrollable_frame(body)
        self._scroll_inner.columnconfigure((0, 1), weight=1, uniform="eq")
        self._refresh()

    def _refresh(self):
        clear_frame(self._scroll_inner)

        conn = sqlite3.connect("database/formaly.db")
        cur  = conn.cursor()
        cur.execute("SELECT id, name, address, capacity, estimated_cost, notes, status FROM venues ORDER BY id")
        venues = cur.fetchall()
        conn.close()

        if not venues:
            tk.Label(self._scroll_inner, text="No venues found.", bg=BG, fg=TEXT_MUTED,
                     font=FONT_H3).grid(row=0, column=0, columnspan=2, pady=60)
            return

        for idx, (vid, name, addr, cap, cost, notes, status) in enumerate(venues):
            r, c = divmod(idx, 2)
            card = tk.Frame(self._scroll_inner, bg=CARD)
            card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

            # Title
            tk.Label(card, text=f"Venue #{idx+1}", bg=CARD, fg=GOLD,
                     font=FONT_H3, anchor="w").pack(fill="x", padx=16, pady=(14, 2))
            tk.Label(card, text=truncate_text(name, 40), bg=CARD, fg=TEXT_LIGHT,
                     font=FONT_BOLD, anchor="w").pack(fill="x", padx=16)
            tk.Label(card, text=truncate_text(addr or "—", 50), bg=CARD, fg=TEXT_MUTED,
                     font=FONT_SMALL, anchor="w").pack(fill="x", padx=16, pady=(0, 8))

            # Capacity / cost bar
            spec = tk.Frame(card, bg=ENTRY)
            spec.pack(fill="x", padx=16, pady=(0, 8))
            tk.Label(spec, text=f"Capacity: {cap} Guests", bg=ENTRY, fg=TEXT_LIGHT,
                     font=FONT_SMALL).pack(side="left", padx=8, pady=6)
            tk.Label(spec, text=f"${cost:,.2f}", bg=ENTRY, fg=GOLD,
                     font=FONT_BOLD).pack(side="right", padx=8)

            # Notes
            tk.Label(card, text=truncate_text(notes or "No description.", 100),
                     bg=CARD, fg=TEXT_MUTED, font=FONT_SMALL,
                     anchor="w", wraplength=360, justify="left").pack(fill="x", padx=16, pady=(0, 10))

            # Calendar icon placeholder
            tk.Label(card, text="📅", bg=CARD, font=("Segoe UI Emoji", 28)).pack(anchor="w", padx=16, pady=(0, 8))
            print("Calendar function where they can see the dates that other events are running is not implemented yet.")

            # Actions
            act = tk.Frame(card, bg=CARD)
            act.pack(fill="x", padx=16, pady=(0, 14))

            approve_btn = tk.Button(act, text="Approve", bg=SUCCESS, fg=TEXT_LIGHT,
                                    font=FONT_BOLD, relief="flat", cursor="hand2",
                                    padx=14, pady=6,
                                    command=lambda vid=vid: self._set_status(vid, "Approved"))
            approve_btn.pack(side="left", padx=(0, 6))

            edit_btn = tk.Button(act, text="Edit", bg=ERROR, fg=TEXT_LIGHT,
                                 font=FONT_BOLD, relief="flat", cursor="hand2",
                                 padx=14, pady=6,
                                 command=lambda vid=vid, n=name, a=addr, cp=cap,
                                         cs=cost, nt=notes, st=status:
                                         self._open_modal(vid, n, a, cp, cs, nt, st))
            edit_btn.pack(side="left")

    def _set_status(self, vid, status):
        conn = sqlite3.connect("database/formaly.db")
        conn.execute("UPDATE venues SET status=? WHERE id=?", (status, vid))
        conn.commit(); conn.close()
        self._refresh()

    def _open_modal(self, vid=None, name="", addr="", cap=100,
                    cost=0.0, notes="", status="Under Review"):
        m = make_modal(self, "Edit Venue" if vid else "Add Venue", 480, 560)
        f = tk.Frame(m, bg=BG, padx=22, pady=22)
        f.pack(fill="both", expand=True)

        n_ent  = modal_field(f, "Name",    name)
        a_ent  = modal_field(f, "Address", addr)

        row = tk.Frame(f, bg=BG)
        row.pack(fill="x", pady=(10, 0))
        row.columnconfigure((0, 1), weight=1)

        tk.Label(row, text="Capacity", bg=BG, fg=GOLD, font=FONT_BOLD).grid(row=0, column=0, sticky="w")
        cap_border = tk.Frame(row, bg=BORDER, padx=1, pady=1)
        cap_border.grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=4)
        cap_ent = tk.Entry(cap_border, bg=ENTRY, fg=TEXT_LIGHT, font=FONT_BODY, bd=0,
                           insertbackground=TEXT_LIGHT)
        cap_ent.pack(fill="x", padx=6, pady=5)
        cap_ent.insert(0, str(cap))

        tk.Label(row, text="Estimated Cost", bg=BG, fg=GOLD, font=FONT_BOLD).grid(row=0, column=1, sticky="w")
        cost_border = tk.Frame(row, bg=BORDER, padx=1, pady=1)
        cost_border.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=4)
        cost_ent = tk.Entry(cost_border, bg=ENTRY, fg=TEXT_LIGHT, font=FONT_BODY, bd=0,
                            insertbackground=TEXT_LIGHT)
        cost_ent.pack(fill="x", padx=6, pady=5)
        cost_ent.insert(0, str(cost))

        tk.Label(f, text="Status", bg=BG, fg=GOLD, font=FONT_BOLD, anchor="w").pack(fill="x", pady=(10, 2))
        s_var = tk.StringVar(value=status)
        ttk.Combobox(f, textvariable=s_var,
                     values=["Under Review","Approved","Rejected"],
                     state="readonly").pack(fill="x", pady=(0, 4))

        nt_ent = modal_field(f, "Notes", notes, height=3)

        def _save():
            n = n_ent.get().strip()
            if not n:
                messagebox.showerror("Error", "Name is required."); return
            try:
                cp = int(cap_ent.get()); cs = float(cost_ent.get())
            except ValueError:
                messagebox.showerror("Error", "Capacity must be integer, cost must be number."); return
            nt = nt_ent.get("1.0", "end-1c").strip()
            conn = sqlite3.connect("database/formaly.db")
            cur  = conn.cursor()
            if vid:
                cur.execute("UPDATE venues SET name=?,address=?,capacity=?,estimated_cost=?,notes=?,status=? WHERE id=?",
                            (n, a_ent.get().strip(), cp, cs, nt, s_var.get(), vid))
            else:
                cur.execute("INSERT INTO venues (name,address,capacity,estimated_cost,notes,status) VALUES (?,?,?,?,?,?)",
                            (n, a_ent.get().strip(), cp, cs, nt, s_var.get()))
            conn.commit(); conn.close()
            m.destroy(); self._refresh()

        btns = tk.Frame(f, bg=BG)
        btns.pack(fill="x", pady=(14, 0))
        tk.Button(btns, text="Save", bg=GOLD, fg=TEXT_LIGHT, font=FONT_BOLD,
                  relief="flat", cursor="hand2", activebackground=GOLD_HOV,
                  padx=16, pady=8, command=_save).pack(side="right")
        tk.Button(btns, text="Cancel", bg=ENTRY, fg=TEXT_LIGHT, font=FONT_BODY,
                  relief="flat", cursor="hand2",
                  padx=16, pady=8, command=m.destroy).pack(side="right", padx=(0, 8))