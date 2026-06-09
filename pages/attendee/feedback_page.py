import tkinter as tk
from tkinter import messagebox
from database.formaly_database_manager import add_feedback, get_formal_data
from utils.styles import (
    BG, CARD, ENTRY, BORDER, GOLD, GOLD_HOV,
    TEXT_LIGHT, TEXT_MUTED, ERROR,
    FONT_BODY, FONT_BOLD, FONT_H2, FONT_H3, FONT_SMALL,
)
from utils.widgets import build_sidebar, navigate, HEADER_H, HDR_BG, LOGO_PATH

_NAV     = ["Invitation", "Feedback"]
_NAV_MAP = {"Invitation": "invitation", "Feedback": "feedback"}

_FIELD_BG = "#E8E8E8"   # light grey text area (matches mockup)


class FormalFeedbackPage(tk.Frame):
    def __init__(self, parent, controller=None, user=None, origin=None):
        super().__init__(parent, bg=BG)
        self.title("Formaly ~ Feedback")
        self.parent    = parent
        self.user      = user
        self._imgs     = []
        self._rating   = 0
        self._star_btns = []
        self.origin = origin or "invitation"
        self._build()

    def _build(self):
        formal = get_formal_data()
        formal_name = formal.get("formal_name") or "Formal Name"

        build_sidebar(self, _NAV, "Feedback",
                      lambda t: navigate(self, self.parent, _NAV_MAP.get(t, t), self.user),
                      self._imgs)

        right = tk.Frame(self, bg=BG)
        right.pack(side="top", fill="both", expand=True)

        # Header — "Attendee Feedback" with white+gold split
        bar = tk.Frame(right, bg=HDR_BG, height=HEADER_H)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        mid = tk.Frame(bar, bg=HDR_BG)
        mid.pack(side="left", padx=24, expand=True, fill="both")
        title_row = tk.Frame(mid, bg=HDR_BG)
        title_row.pack(anchor="w", pady=(28, 0))
        tk.Label(title_row, text="Attendee ", bg=HDR_BG, fg=TEXT_LIGHT,
                 font=FONT_H2).pack(side="left")
        tk.Label(title_row, text="Feedback",  bg=HDR_BG, fg=GOLD,
                 font=FONT_H2).pack(side="left")
        icons = tk.Frame(bar, bg=HDR_BG)
        icons.pack(side="right", padx=24)
        tk.Label(icons, text="🔔", bg=HDR_BG, fg=TEXT_LIGHT, font=("Segoe UI Emoji", 18)).pack(side="left", padx=6)
        tk.Label(icons, text="👤", bg=HDR_BG, fg=GOLD,       font=("Segoe UI Emoji", 22)).pack(side="left", padx=6)

        # Main card
        card = tk.Frame(right, bg=CARD)
        card.pack(fill="both", expand=True, padx=22, pady=18)

        tk.Label(card, text=f"{formal_name} Feedback", bg=CARD, fg=GOLD,
                 font=FONT_H3).pack(pady=(20, 16))
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(0, 16))

        # Overall Feedback label + stars
        star_row = tk.Frame(card, bg=CARD)
        star_row.pack(padx=24, pady=(0, 6), anchor="w")
        tk.Label(star_row, text="Overall Feedback:", bg=CARD, fg=TEXT_LIGHT,
                 font=FONT_BOLD).pack(side="left", padx=(0, 20))

        stars_frame = tk.Frame(star_row, bg=CARD)
        stars_frame.pack(side="left")
        for i in range(1, 6):
            btn = tk.Button(stars_frame, text="☆", bg=CARD, fg=GOLD,
                            font=("Segoe UI Emoji", 22), relief="flat", bd=0,
                            cursor="hand2", activebackground=CARD,
                            command=lambda v=i: self._set_rating(v))
            btn.pack(side="left", padx=2)
            self._star_btns.append(btn)

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(10, 14))

        # Improvements text area — light grey as in mockup
        txt_frame = tk.Frame(card, bg=_FIELD_BG)
        txt_frame.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self._txt = tk.Text(txt_frame, bg=_FIELD_BG, fg="#888888",
                            font=FONT_BODY, relief="flat", bd=0,
                            wrap="word", insertbackground="#333")
        self._txt.pack(fill="both", expand=True, padx=12, pady=10)
        _ph = "What would you improve?"
        self._txt.insert("1.0", _ph)

        def _txt_in(e):
            if self._txt.get("1.0", "end-1c") == _ph:
                self._txt.delete("1.0", "end")
                self._txt.config(fg=TEXT_MUTED)
        def _txt_out(e):
            if not self._txt.get("1.0", "end-1c").strip():
                self._txt.insert("1.0", _ph)
                self._txt.config(fg="#888888")
        self._txt.bind("<FocusIn>",  _txt_in)
        self._txt.bind("<FocusOut>", _txt_out)

        # Submit button
        sub = tk.Button(card, text="SUBMIT", bg=GOLD, fg=TEXT_LIGHT,
                        font=FONT_BOLD, relief="flat", cursor="hand2",
                        width=20, activebackground=GOLD_HOV,
                        command=self._submit)
        sub.pack(pady=(0, 20), ipady=8)
        sub.bind("<Enter>", lambda e: sub.config(bg=GOLD_HOV))
        sub.bind("<Leave>", lambda e: sub.config(bg=GOLD))

    def _set_rating(self, value):
        self._rating = value
        for i, btn in enumerate(self._star_btns):
            btn.config(text="★" if i < value else "☆")

    def _submit(self):
        _ph = "What would you improve?"
        improvements = self._txt.get("1.0", "end-1c").strip()
        if improvements == _ph:
            improvements = ""
        if self._rating == 0 and not improvements:
            messagebox.showwarning("Required", "Please provide a rating or write your feedback.")
            return
        try:
            add_feedback(str(self._rating), improvements)
            messagebox.showinfo("Thank You", "Your feedback has been submitted.")
            navigate(self, self.parent, "invitation", self.user)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))