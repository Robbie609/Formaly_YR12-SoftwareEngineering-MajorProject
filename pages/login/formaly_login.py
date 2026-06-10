# Imports
import tkinter as tk
from tkinter import messagebox
from database.formaly_database_manager import get_user
from utils.helpers import center_window, PlaceholderEntry
from utils.validators import validate_login
from utils.styles import (
    CREAM, CREAM_FIELD, GOLD, GOLD_HOV,
    BG as PANEL_BLACK,
    TEXT_DARK, TEXT_MUTED, TEXT_ON_GOLD,
    SUCCESS, ERROR,
    FONT_BRAND, FONT_H1, FONT_BODY, FONT_BOLD, FONT_SMALL,
    ROLE_MAP,
)

# Logo Variable
LOGO_PATH = "assets/Logo1.png"

# Fonts used
_F_LABEL  = ("Segoe UI", 9)
_F_ROLE   = ("Segoe UI", 10, "bold")
_F_SUBMIT = ("Segoe UI", 12, "bold")
_F_LINK   = ("Segoe UI", 10)

# Class for the Login Page
class FormalyLoginApp(tk.Tk):

    # Setting the basic settings of the window
    def __init__(self, parent=None):
        super().__init__()
        self.title("Formaly")
        self.configure(bg=PANEL_BLACK)
        self.logo_image = tk.PhotoImage(file=LOGO_PATH) # Loads the image
        self.iconphoto(False, self.logo_image)         
        self.geometry("1200x700")
        self.minsize(960, 600)
        self.resizable(True, True)
        center_window(self, 1200, 700)
        self.current_user  = None
        self.selected_role = None
        self.parent        = parent
        self._pw_visible   = False
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
        panel.pack(side="left", fill="both")
        panel.pack_propagate(False)
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
            # I want to double the image's size
            tk.Label(logo_frame, image=self._logo, bg=PANEL_BLACK).pack(expand=True)
        except tk.TclError:
            tk.Label(logo_frame, text="🎩", bg=PANEL_BLACK, fg=GOLD,
                     font=("Segoe UI Emoji", 72)).pack(expand=True)

    # Right panel with buttons and entry fields for login
    # Creating the right section of the window
    def _build_right(self):
        panel = tk.Frame(self, bg=CREAM)
        panel.pack(side="right", fill="both", expand=True)
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(0, weight=1)

        form = tk.Frame(panel, bg=CREAM)
        form.pack(expand=True)
        self._build_form(form)

    # Setting it as a form
    def _build_form(self, f):
        tk.Label(f, text="Log In", bg=CREAM, fg=TEXT_DARK,
                 font=FONT_H1).pack(pady=(0, 6))

        # Line with link to register page
        row = tk.Frame(f, bg=CREAM)
        row.pack()
        tk.Label(row, text="Don't have an account? ", bg=CREAM,
                 fg=TEXT_MUTED, font=_F_LINK).pack(side="left")
        
        # Link to register page
        lnk = tk.Label(row, text="Sign up", bg=CREAM, fg=GOLD,
                       font=(_F_LINK[0], _F_LINK[1], "bold"), cursor="hand2")
        lnk.pack(side="left")
        lnk.bind("<Button-1>", lambda e: self._open_register())

        # Back to normal text
        tk.Label(row, text=" here", bg=CREAM, fg=TEXT_MUTED,
                 font=_F_LINK).pack(side="left")
        tk.Frame(f, bg=CREAM, height=18).pack()

        # Role buttons
        self._build_roles(f)
        tk.Frame(f, bg=CREAM, height=20).pack()

        # USERNAME field
        self._spaced_label(f, "USERNAME")
        usr_widget = tk.Entry(f, bg=CREAM_FIELD, fg=TEXT_MUTED,
                              font=_F_LINK, relief="solid", bd=1,
                              insertbackground=TEXT_DARK, width=50)
        usr_widget.pack(ipady=12)
        self._usr_ph = PlaceholderEntry(usr_widget, " Enter your username",
                                        fg_normal=TEXT_DARK, fg_placeholder=TEXT_MUTED)
        self._usr_widget = usr_widget

        tk.Frame(f, bg=CREAM, height=12).pack()

        # PASSWORD field with eye toggle
        self._spaced_label(f, "PASSWORD")
        pw_container = tk.Frame(f, bg=CREAM_FIELD, bd=1, relief="solid")
        pw_container.pack()
        pw_widget = tk.Entry(pw_container, bg=CREAM_FIELD, fg=TEXT_MUTED,
                             font=_F_LINK, relief="flat", bd=0, show="",
                             insertbackground=TEXT_DARK, width=50)
        pw_widget.pack(side="left", ipady=12, padx=(8, 0))
        self._pw_ph = PlaceholderEntry(pw_widget, "Enter your password",
                                       fg_normal=TEXT_DARK, fg_placeholder=TEXT_MUTED,
                                       show_char="●")
        self._pw_widget = pw_widget
        eye = tk.Button(pw_container, text="👁", bg=CREAM_FIELD, fg=TEXT_MUTED,
                        font=("Segoe UI Emoji", 11), relief="flat", bd=0,
                        cursor="hand2", command=self._toggle_pw)
        eye.pack(side="left", padx=(4, 8))

        # When enter key is pressed, it will trigger the login function
        pw_widget.bind("<Return>", lambda e: self._do_login())
        tk.Frame(f, bg=CREAM, height=26).pack()

        # Log in button
        self.login_btn = tk.Button(
            f, text="Log in", bg=GOLD, fg=TEXT_ON_GOLD,
            font=_F_SUBMIT, relief="flat", cursor="hand2", width=50,
            activebackground=GOLD_HOV, activeforeground=TEXT_ON_GOLD,
            command=self._do_login
        )
        self.login_btn.pack(ipady=13)

        # Button hover effects
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg=GOLD_HOV))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg=GOLD))

        # Status on login process line
        self.status_lbl = tk.Label(f, text="", bg=CREAM, fg=ERROR,
                                   font=FONT_SMALL, wraplength=440)
        self.status_lbl.pack(pady=(8, 0))

    # This function creates the role selection buttons
    def _build_roles(self, parent):
        row = tk.Frame(parent, bg=CREAM)
        row.pack()
        self._role_btns = {}

        # This sets a button for each role
        for role in ("Admin", "Planner", "Support"):
            btn = tk.Button(
                row, text=role.upper(), bg=GOLD, fg=TEXT_ON_GOLD,
                font=_F_ROLE, relief="flat", cursor="hand2", width=13,
                activebackground=GOLD_HOV, activeforeground=TEXT_ON_GOLD,
                command=lambda r=role: self._select_role(r)
            )
            btn.pack(side="left", padx=5, ipady=11)
            self._role_btns[role] = btn

    # This function manages the state of the role selection buttons, ensuring only one can be active at a time
    def _select_role(self, role):
        self.selected_role = role
        for r, btn in self._role_btns.items():
            btn.config(bg=GOLD_HOV if r == role else GOLD,
                       relief="sunken" if r == role else "flat")

    # This function creates the confirm password field in the registration page
    def _spaced_label(self, parent, text):
        tk.Label(parent, text=text, bg=CREAM, fg=TEXT_MUTED,
                 font=_F_LABEL).pack(pady=(0, 5))

    # This function toggles the visibility of the password field when the eye icon is clicked
    def _toggle_pw(self):
        if self._pw_ph.is_placeholder():
            return
        self._pw_visible = not self._pw_visible
        self._pw_widget.config(show="" if self._pw_visible else "●")

    # This function manages the login process when the login button is clicked
    def _do_login(self):
        if not self.selected_role:
            self._show_status("Please select a role.", ERROR)
            return

        # Read and validate inputs
        username = self._usr_ph.get_value()
        password = self._pw_ph.get_value()

        # Validate inputs before attempting login
        ok, msg = validate_login(username, password)
        if not ok:
            self._show_status(msg, ERROR)
            return

        # gets the account from the database
        try:
            user = get_user(username, password)
        except Exception as exc:
            self._show_status(f"Database error: {exc}", ERROR)
            return

        # If no user is found with the provided credentials, show an error message
        if not user:
            self._show_status("Incorrect username or password.", ERROR)
            return

        # Check if the user's role matches the selected role
        db_role  = str(user["Role"]).strip().lower()
        expected = ROLE_MAP.get(self.selected_role, "")

        # If the role from the database doesn't match the expected role based on the button selection, show an error message
        if db_role != expected:
            self._show_status("Account not authorised for the selected role.", ERROR)
            return

        # If all checks pass, set the current user and open the appropriate dashboard based on their role
        self.current_user = user
        self._show_status("Login successful!", SUCCESS)
        self.after(500, lambda: self._open_dashboard(db_role))

    # This function opens the dashboard corresponding to the user's role
    def _open_dashboard(self, role):
        try:
            # Depending on the role, it imports and opens the corresponding dashboard page
            if role == "admin":
                from pages.admin.admin_dashboard import AdminDashboard
                dash = AdminDashboard(self, user=self.current_user)
            elif role == "planner":
                from pages.planner.planner_dashboard import PlannerDashboard
                dash = PlannerDashboard(self, user=self.current_user)
            elif role == "helper":
                from pages.support.support_dashboard import SupportDashboard
                dash = SupportDashboard(self, user=self.current_user)
            else:
                self._show_status(f"Unknown role: {role}", ERROR)
                return
            
            # If the dashboard opens successfully, the login window is hidden and the dashboard is shown
            self.status_lbl.config(text="")
            dash.place(relwidth=1, relheight=1)
            dash.lift()

        # If there's an error while opening the dashboard, it shows an error message
        except Exception as exc:
            self._show_status(f"Error opening dashboard: {exc}", ERROR)

    # This function opens the registration page when the "Sign up" link is clicked
    def _open_register(self):
        try:
            from pages.login.formaly_register import FormalyRegisterApp
            FormalyRegisterApp(self)
            self.withdraw()
        except Exception as exc:
            messagebox.showerror("Error", f"Could not open register: {exc}")

    # This function updates the status label with a message and colour
    def _show_status(self, msg, colour):
        self.status_lbl.config(text=msg, fg=colour)
        if colour == SUCCESS:
            self.after(2000, lambda: self.status_lbl.config(text=""))