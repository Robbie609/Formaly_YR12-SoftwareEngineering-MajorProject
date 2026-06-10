# Imports
import tkinter as tk
from tkinter import messagebox
import sqlite3
from database.formaly_database_manager import get_formal_data
from utils.styles import (
    BG, CARD, ENTRY, BORDER, GOLD, GOLD_HOV,
    TEXT_LIGHT, TEXT_MUTED,
    FONT_BODY, FONT_BOLD, FONT_H2, FONT_H3, FONT_SMALL,
)
from utils.widgets import build_sidebar, build_header, navigate, HEADER_H, HDR_BG, LOGO_PATH

_FIELD_BG = "#3A3A3A"   # light-grey field bg from mockup


class FormalInvitationPage(tk.Frame):
    # Initialising the invitation page
    def __init__(self, parent, controller=None, user=None, origin=None):
        super().__init__(parent, bg=BG)
        self.parent = parent
        self.user   = user
        self._imgs  = []
        self._plus_visible = False
        self._build()
        self.origin = origin or "admin"
    # Builds main UI layout
    def _build(self):
        formal = get_formal_data()
        bar = tk.Frame(self, bg=HDR_BG, height=HEADER_H)
        bar.pack(side="top", fill="x")
        bar.pack_propagate(False)
        mid = tk.Frame(bar, bg=HDR_BG)
        mid.pack(side="left", padx=24, expand=True, fill="both")
        tk.Label(mid, text="Attendee Invitation", bg=HDR_BG, fg=TEXT_LIGHT,
                 font=FONT_H2, anchor="w").pack(anchor="w", pady=(28, 0))
        icons = tk.Frame(bar, bg=HDR_BG)
        icons.pack(side="right", padx=24)
        tk.Label(icons, text="🔔", bg=HDR_BG, fg=TEXT_LIGHT, font=("Segoe UI Emoji", 18)).pack(side="left", padx=6)
        tk.Label(icons, text="👤", bg=HDR_BG, fg=GOLD,       font=("Segoe UI Emoji", 22)).pack(side="left", padx=6)

        # Right content area
        right = tk.Frame(self, bg=BG)
        right.pack(side="top", fill="both", expand=True)

        # Re place header inside right
        bar.destroy()
        bar2 = tk.Frame(right, bg=HDR_BG, height=HEADER_H)
        bar2.pack(fill="x")
        bar2.pack_propagate(False)
        mid2 = tk.Frame(bar2, bg=HDR_BG)
        mid2.pack(side="left", padx=24, expand=True, fill="both")
        tk.Label(mid2, text="Attendee", bg=HDR_BG, fg=TEXT_LIGHT,
                 font=FONT_H2, anchor="w").pack(anchor="w", pady=(28, 0))
        icons2 = tk.Frame(bar2, bg=HDR_BG)
        icons2.pack(side="right", padx=24)
        tk.Label(icons2, text="🔔", bg=HDR_BG, fg=TEXT_LIGHT, font=("Segoe UI Emoji", 18)).pack(side="left", padx=6)
        tk.Label(icons2, text="👤", bg=HDR_BG, fg=GOLD,       font=("Segoe UI Emoji", 22)).pack(side="left", padx=6)

        # Scrollable body
        body_outer = tk.Frame(right, bg=BG)
        body_outer.pack(fill="both", expand=True)

        # Central card
        card = tk.Frame(body_outer, bg=CARD)
        card.place(relx=0.04, rely=0.04, relwidth=0.92, relheight=0.92)

        # Card content
        col = tk.Frame(card, bg=CARD)
        col.place(relx=0.5, rely=0.5, anchor="center")

        school_name = formal.get("school") or "Your School"
        formal_name = formal.get("formal_name") or "Formal Name"
        # Connects to the database
        conn = sqlite3.connect("database/formaly.db")
        cur  = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM attendees")
        attending = cur.fetchone()[0]
        conn.close()

        # Main event details
        tk.Label(col, text=f"{school_name} Invites you to", bg=CARD, fg=TEXT_LIGHT,
                 font=FONT_BODY).pack()
        tk.Label(col, text=formal_name, bg=CARD, fg=GOLD,
                 font=("Segoe UI", 22, "bold")).pack(pady=(4, 8))
        tk.Label(col, text=f"{attending} people attending", bg=CARD, fg=TEXT_MUTED,
                 font=FONT_SMALL).pack()
        tk.Label(col, text="Date: YYYY/MM/DD", bg=CARD, fg=TEXT_MUTED,
                 font=FONT_SMALL).pack(pady=2)
        tk.Label(col, text="Time: HH:MM", bg=CARD, fg=TEXT_MUTED,
                 font=FONT_SMALL).pack(pady=(2, 14))

        # Name entry
        self._name_ent = tk.Entry(col, bg=_FIELD_BG, fg=TEXT_MUTED,
                                  font=FONT_BODY, relief="flat",
                                  insertbackground=TEXT_LIGHT, width=46)
        self._name_ent.pack(ipady=10)
        self._name_ent.insert(0, "Enter Attendee's Name")
        self._name_ent.bind("<FocusIn>",  self._name_in)
        self._name_ent.bind("<FocusOut>", self._name_out)

        # Add Plus One toggle
        self._plus_btn = tk.Button(col, text="Add Plus One",
                                   bg=GOLD, fg=TEXT_LIGHT, font=FONT_BOLD,
                                   relief="flat", cursor="hand2", width=24,
                                   activebackground=GOLD_HOV,
                                   command=self._toggle_plus)
        self._plus_btn.pack(pady=(12, 0), ipady=8)
        self._plus_btn.bind("<Enter>", lambda e: self._plus_btn.config(bg=GOLD_HOV))
        self._plus_btn.bind("<Leave>", lambda e: self._plus_btn.config(bg=GOLD))

        # Plus-one name (hidden until toggled)
        self._plus_frame = tk.Frame(col, bg=CARD)
        self._plus_ent = tk.Entry(self._plus_frame, bg=_FIELD_BG, fg=TEXT_MUTED,
                                  font=FONT_BODY, relief="flat",
                                  insertbackground=TEXT_LIGHT, width=46)
        self._plus_ent.pack(ipady=10)
        self._plus_ent.insert(0, "Enter Name")

        # Submit
        sub_btn = tk.Button(col, text="SUBMIT", bg=GOLD, fg=TEXT_LIGHT,
                            font=FONT_BOLD, relief="flat", cursor="hand2",
                            width=46, activebackground=GOLD_HOV,
                            command=self._submit)
        sub_btn.pack(pady=(10, 0), ipady=10)
        sub_btn.bind("<Enter>", lambda e: sub_btn.config(bg=GOLD_HOV))
        sub_btn.bind("<Leave>", lambda e: sub_btn.config(bg=GOLD))

        # Feedback link
        tk.Label(col, text="Once the event is finished", bg=CARD, fg=TEXT_MUTED,
                 font=FONT_SMALL).pack(pady=(16, 4))
        fb_btn = tk.Button(col, text="FEEDBACK", bg=GOLD, fg=TEXT_LIGHT,
                           font=FONT_BOLD, relief="flat", cursor="hand2",
                           width=18, activebackground=GOLD_HOV,
                           command=lambda: navigate(self, self.parent, "feedback", self.user))
        fb_btn.pack(ipady=8)
        fb_btn.bind("<Enter>", lambda e: fb_btn.config(bg=GOLD_HOV))
        fb_btn.bind("<Leave>", lambda e: fb_btn.config(bg=GOLD))

    # Enter Attendee's name focus in
    def _name_in(self, e):
        if self._name_ent.get() == "Enter Attendee's Name":
            self._name_ent.delete(0, "end")
            self._name_ent.config(fg=TEXT_LIGHT)
    # Enter Attendee's name focus out
    def _name_out(self, e):
        if not self._name_ent.get().strip():
            self._name_ent.insert(0, "Enter Attendee's Name")
            self._name_ent.config(fg=TEXT_MUTED)
    # Toggling the plus one 
    def _toggle_plus(self):
        self._plus_visible = not self._plus_visible
        if self._plus_visible:
            self._plus_frame.pack(pady=(8, 0))
            self._plus_btn.config(text="Remove Plus One")
        else:
            self._plus_frame.pack_forget()
            self._plus_btn.config(text="Add Plus One")
    # Submit the data to the database
    def _submit(self):
        name = self._name_ent.get().strip()
        # Empty state validation
        if not name or name == "Enter Attendee's Name":
            messagebox.showwarning("Missing", "Please enter the attendee's name.")
            return
        try:
            conn = sqlite3.connect("database/formaly.db")
            cur  = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO attendees (name, plus_one, paid, attendance) VALUES (?, ?, 0, 0)",
                        (name, 1 if self._plus_visible else 0))
            conn.commit()
            conn.close()
            messagebox.showinfo("Submitted", f"Attendance recorded for {name}.")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))