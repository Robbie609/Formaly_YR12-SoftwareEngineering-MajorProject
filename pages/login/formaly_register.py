# Imports
import tkinter as tk
from tkinter import messagebox
from utils.helpers import center_window, PlaceholderEntry
from utils.styles import (
    CREAM, CREAM_FIELD, GOLD, GOLD_HOV,
    BG as PANEL_BLACK,
    TEXT_DARK, TEXT_MUTED, TEXT_ON_GOLD,
    ERROR,
    FONT_BRAND, FONT_H1, FONT_SMALL,
    ROLE_MAP,
)

# Logo Variable
LOGO_PATH = "assets/Logo1.png"

# Fonts used
_F_LABEL  = ("Segoe UI",  9)
_F_ROLE   = ("Segoe UI", 10, "bold")
_F_SUBMIT = ("Segoe UI", 12, "bold")
_F_LINK   = ("Segoe UI", 10)

# Class for the registration page
class FormalyRegisterApp(tk.Toplevel):

    # Setting the basic settings of the window
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Formaly")
        self.configure(bg=PANEL_BLACK)
        self.geometry("1200x700")
        self.minsize(960, 600)
        self.resizable(True, True)
        self.parent = parent
        center_window(self, 1200, 700)
        self.protocol("WM_DELETE_WINDOW", self._go_back)
        self._pw_visible  = False
        self._cf_visible  = False
        self._build()

    # Setting up the layout of the page with two columns, left for logo and right for login form
    def _build(self):
        self.columnconfigure(0, weight=0, minsize=500)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self._build_left()
        self._build_right()

    # Left panel with logo
    def _build_left(self):
        panel = tk.Frame(self, bg=PANEL_BLACK, width=500)
        panel.grid(row=0, column=0, sticky="nsew")
        panel.grid_propagate(False)
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(0, weight=0)
        panel.rowconfigure(1, weight=1)

        # Title
        tk.Label(
            panel, text="Formaly",
            bg=PANEL_BLACK, fg=GOLD,
            font=FONT_BRAND, anchor="center"
        ).pack(fill="x", padx=30, pady=(36, 0))

        # Logo Image
        logo_frame = tk.Frame(panel, bg=PANEL_BLACK)
        logo_frame.pack(fill="both", expand=True)
        logo_frame.columnconfigure(0, weight=1)
        logo_frame.rowconfigure(0, weight=1)
        try:
            self._logo = tk.PhotoImage(file=LOGO_PATH)
            tk.Label(logo_frame, image=self._logo, bg=PANEL_BLACK
                     ).grid(row=0, column=0)
        except tk.TclError:
            tk.Label(logo_frame, text="🎩", bg=PANEL_BLACK, fg=GOLD,
                     font=("Segoe UI Emoji", 72)).grid(row=0, column=0)

    # Right panel with buttons and entry fields for login
    # Creating the right section of the window
    def _build_right(self):
        panel = tk.Frame(self, bg=CREAM)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(0, weight=1)

        form = tk.Frame(panel, bg=CREAM)
        form.grid(row=0, column=0)
        self._build_form(form)

    # Setting it as a form
    def _build_form(self, f):
        # "Sign Up" heading
        tk.Label(f, text="Sign Up", bg=CREAM, fg=TEXT_DARK,
                 font=FONT_H1).pack(pady=(0, 6))
        
        # Line with link to login page
        row = tk.Frame(f, bg=CREAM)
        row.pack()
        tk.Label(row, text="Already have an account? ", bg=CREAM,
                 fg=TEXT_MUTED, font=_F_LINK).pack(side="left")
        
        # Link to login page
        lnk = tk.Label(row, text="Log In", bg=CREAM, fg=GOLD,
                       font=(_F_LINK[0], _F_LINK[1], "bold"), cursor="hand2")
        lnk.pack(side="left")
        lnk.bind("<Button-1>", lambda e: self._go_back())

        # Back to normal text
        tk.Label(row, text=" here", bg=CREAM, fg=TEXT_MUTED,
                 font=_F_LINK).pack(side="left")
        
        tk.Frame(f, bg=CREAM, height=16).pack()

        # Role buttons
        role_row = tk.Frame(f, bg=CREAM)
        role_row.pack()
        for role in ("Admin", "Planner", "Support"):
            tk.Button(
                role_row, text=role.upper(), bg=GOLD, fg=TEXT_ON_GOLD,
                font=_F_ROLE, relief="flat", cursor="hand2", width=13,
                activebackground=GOLD_HOV, activeforeground=TEXT_ON_GOLD,
            ).pack(side="left", padx=5, ipady=11)

        tk.Frame(f, bg=CREAM, height=16).pack()

        # USERNAME field
        self._spaced_label(f, "USERNAME")
        usr_w = tk.Entry(f, bg=CREAM_FIELD, fg=TEXT_MUTED, font=_F_LINK,
                         relief="solid", bd=1, insertbackground=TEXT_DARK, width=50)
        usr_w.pack(ipady=12)
        PlaceholderEntry(usr_w, "Enter your username",
                         fg_normal=TEXT_DARK, fg_placeholder=TEXT_MUTED)

        tk.Frame(f, bg=CREAM, height=10).pack()

        # PASSWORD field with eye toggle
        self._spaced_label(f, "PASSWORD")
        pw_container = tk.Frame(f, bg=CREAM_FIELD, bd=1, relief="solid")
        pw_container.pack()
        self._pw_w = tk.Entry(pw_container, bg=CREAM_FIELD, fg=TEXT_MUTED,
                              font=_F_LINK, relief="flat", bd=0, show="",
                              insertbackground=TEXT_DARK, width=50)
        self._pw_w.pack(side="left", ipady=12, padx=(8, 0))
        self._pw_ph = PlaceholderEntry(self._pw_w, "Enter your password",
                                       fg_normal=TEXT_DARK, fg_placeholder=TEXT_MUTED,
                                       show_char="●")
        tk.Button(pw_container, text="👁", bg=CREAM_FIELD, fg=TEXT_MUTED,
                  font=("Segoe UI Emoji", 11), relief="flat", bd=0,
                  cursor="hand2",
                  command=self._toggle_pw).pack(side="left", padx=(4, 8))

        tk.Frame(f, bg=CREAM, height=10).pack()

        # RE-ENTER PASSWORD field with eye toggle
        self._spaced_label(f, "RE - ENTER PASSWORD")
        cf_container = tk.Frame(f, bg=CREAM_FIELD, bd=1, relief="solid")
        cf_container.pack()
        self._cf_w = tk.Entry(cf_container, bg=CREAM_FIELD, fg=GOLD,
                              font=_F_LINK, relief="flat", bd=0, show="",
                              insertbackground=TEXT_DARK, width=55)
        self._cf_w.pack(side="left", ipady=12, padx=(8, 0))
        self._cf_ph = PlaceholderEntry(self._cf_w, "Enter your password again",
                                       fg_normal=TEXT_DARK, fg_placeholder=GOLD,
                                       show_char="*")
        tk.Button(cf_container, text="👁", bg=CREAM_FIELD, fg=TEXT_MUTED,
                  font=("Segoe UI Emoji", 11), relief="flat", bd=0,
                  cursor="hand2",
                  command=self._toggle_cf).pack(side="left", padx=(4, 8))

        tk.Frame(f, bg=CREAM, height=22).pack()

        # Sign Up button
        signup_btn = tk.Button(
            f, text="Sign Up", bg=GOLD, fg=TEXT_ON_GOLD,
            font=_F_SUBMIT, relief="flat", cursor="hand2", width=50,
            activebackground=GOLD_HOV, activeforeground=TEXT_ON_GOLD,
            command=self._on_signup
        )
        signup_btn.pack(ipady=13)

        # Button hover effects
        signup_btn.bind("<Enter>", lambda e: signup_btn.config(bg=GOLD_HOV))
        signup_btn.bind("<Leave>", lambda e: signup_btn.config(bg=GOLD))

        # Status on sign up process line
        self.status_lbl = tk.Label(f, text="", bg=CREAM, fg=ERROR,
                                   font=FONT_SMALL, wraplength=440)
        self.status_lbl.pack(pady=(8, 0))

    # This function creates a label with some spacing below it, used for the form fields
    def _spaced_label(self, parent, text):
        tk.Label(parent, text=text, bg=CREAM, fg=TEXT_MUTED,
                 font=_F_LABEL).pack(pady=(0, 5))
        
    # This function toggles the visibility of the password field when the eye button is clicked
    def _toggle_pw(self):
        if self._pw_ph.is_placeholder():
            return
        self._pw_visible = not self._pw_visible
        self._pw_w.config(show="" if self._pw_visible else "●")

    # This function toggles the visibility of the confirm password field when the eye button is clicked
    def _toggle_cf(self):
        if self._cf_ph.is_placeholder():
            return
        self._cf_visible = not self._cf_visible
        self._cf_w.config(show="" if self._cf_visible else "●")

    # This function is called when the "Sign Up" button is clicked, currently it just shows an info message that registration is unavailable
    def _on_signup(self):
        messagebox.showinfo(
            "Registration Unavailable",
            "At this moment, registration is unavailable. This is a demo version of the registration page."
        )

    # This function is called when the user clicks the "Log In" link or closes the registration window, it destroys the registration window and shows the parent login window again.
    def _go_back(self):
        self.destroy()
        self.parent.deiconify()