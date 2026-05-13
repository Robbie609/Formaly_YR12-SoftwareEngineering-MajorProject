import tkinter as tk
import hashlib
import time
import sqlite3
con = sqlite3.connect("Authentication.db")
cur = con.cursor()
cur.execute("CREATE TABLE Credentials(Member_ID, Username, Password_hashed, Email, School, Event_Name)")
res = cur.execute("SELECT Username FROM Credentials")
res.fetchone()

# --- Configuration & Mock Data ---
BG_COLOR = "#0B0B0B"
FG_PRIMARY = "#FFD24A"
FG_SECONDARY = "#C0C0C0"
BG_SECONDARY = "#1A1A1A"
BG_ENTRY = "#0A0A0A"

ROLES = ["Student Planner", "Support Staff", "Administrator"]

# Default accounts
password_student = hashlib.sha256("EBHSPlanner".encode()).hexdigest()
password_support = hashlib.sha256("EBHSHelper".encode()).hexdigest()
password_admin = hashlib.sha256("EBHSAdmin".encode()).hexdigest()

VALID_ACCOUNTS = {
    "Student Planner": {
        "username": "Rowan",
        "email": "rowan@example.com",
        "password_hash": password_student
    },
    "Support Staff": {
        "username": "Rigved",
        "email": None,
        "password_hash": password_support
    },
    "Administrator": {
        "username": "Schadel",
        "email": "schadel@example.com",
        "school": "Sydney Boys High School",
        "password_hash": password_admin
    }
}


class FormalyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Formaly - Login")
        self.geometry("900x600")
        self.configure(bg=BG_COLOR)
        self.resizable(True, True)

        self.eval('tk::PlaceWindow . center')

        self.current_role = tk.StringVar(value=ROLES[0])
        self.container = None

        self._build_login_ui()

    # ---------------------------------------------------------
    # Utility Helpers
    # ---------------------------------------------------------

    def clear_container(self):
        if self.container is not None:
            self.container.destroy()
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill=tk.BOTH, expand=True)

    def select_role(self, role):
        self.current_role.set(role)
        for r, btn in self.role_buttons.items():
            if r == role:
                btn.config(bg=FG_PRIMARY, fg=BG_COLOR)
            else:
                btn.config(bg=BG_SECONDARY, fg=FG_SECONDARY)

    def on_btn_hover(self, btn, role):
        if self.current_role.get() != role:
            btn.config(bg="#2A2A2A")

    def on_btn_leave(self, btn, role):
        if self.current_role.get() != role:
            btn.config(bg=BG_SECONDARY)

    def on_focus(self, entry):
        entry.config(highlightthickness=1, highlightbackground=FG_PRIMARY, highlightcolor=FG_PRIMARY)

    def on_focus_out(self, entry):
        entry.config(highlightthickness=1, highlightbackground="#333333", highlightcolor="#333333")

    def shake_window(self):
        original_x = self.winfo_x()
        original_y = self.winfo_y()
        offsets = [-10, 10, -10, 10, -5, 5, 0]

        for offset in offsets:
            self.geometry(f"+{original_x + offset}+{original_y}")
            self.update()
            time.sleep(0.05)

    # ---------------------------------------------------------
    # Password Strength + Toggle
    # ---------------------------------------------------------

    def evaluate_password_strength(self, password):
        score = 0
        if len(password) >= 8:
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*()-_=+[]{};:,.<>?/\\|" for c in password):
            score += 1

        if score <= 1:
            return "Weak", "#FF4C4C"
        elif score == 2:
            return "Medium", "#FFB84C"
        else:
            return "Strong", "#4CFF72"

    def update_strength_meter(self, event=None):
        password = self.reg_password_entry.get()
        strength, color = self.evaluate_password_strength(password)
        self.strength_label.config(text=f"Strength: {strength}", fg=color)

    def toggle_password(self, entry, btn):
        if entry.cget("show") == "*":
            entry.config(show="")
            btn.config(text="Hide")
        else:
            entry.config(show="*")
            btn.config(text="Show")

    # ---------------------------------------------------------
    # LOGIN UI
    # ---------------------------------------------------------

    def _build_login_ui(self):
        self.clear_container()

        # Left Panel
        left_panel = tk.Frame(self.container, bg="#111111", width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="Formaly", font=("Montserrat", 26, "bold"),
                 bg="#111111", fg=FG_PRIMARY).pack(pady=(30, 10))

        logo_img = tk.PhotoImage(file=r"C:\Users\2rm2j\Documents\Software\Project\Formaly_YR12-SoftwareEngineering-MajorProject\Logo.png")
        tk.Label(left_panel, image=logo_img, bg="#111111").pack()
        left_panel.logo_img = logo_img

        # Right Panel
        right_panel = tk.Frame(self.container, bg=BG_COLOR)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=40, pady=40)

        tk.Label(right_panel, text="WELCOME BACK!", font=("Calibri", 20, "bold"),
                 bg=BG_COLOR, fg="white").pack(anchor="w", pady=(20, 20))

        # Role Selector
        tk.Label(right_panel, text="SELECT ROLE", font=("Calibri", 10, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w")

        role_frame = tk.Frame(right_panel, bg=BG_COLOR)
        role_frame.pack(fill=tk.X, pady=(10, 15))

        self.role_buttons = {}
        for role in ROLES:
            btn = tk.Button(
                role_frame, text=role, font=("Calibri", 10),
                bg=BG_SECONDARY if role != self.current_role.get() else FG_PRIMARY,
                fg=FG_SECONDARY if role != self.current_role.get() else BG_COLOR,
                relief="flat", cursor="hand2",
                command=lambda r=role: self.select_role(r)
            )
            btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
            self.role_buttons[role] = btn

            btn.bind("<Enter>", lambda e, b=btn, r=role: self.on_btn_hover(b, r))
            btn.bind("<Leave>", lambda e, b=btn, r=role: self.on_btn_leave(b, r))

        # Username
        tk.Label(right_panel, text="USERNAME", font=("Calibri", 16, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="nw")
        self.username_entry = tk.Entry(right_panel, font=("Calibri", 12),
                                       bg=BG_ENTRY, fg="white",
                                       insertbackground=FG_PRIMARY, relief="flat")
        self.username_entry.pack(fill=tk.X, pady=(5, 15), ipady=8)

        # Password
        tk.Label(right_panel, text="PASSWORD", font=("Calibri", 16, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w")
        self.password_entry = tk.Entry(right_panel, font=("Calibri", 12),
                                       bg=BG_ENTRY, fg="white",
                                       insertbackground=FG_PRIMARY, relief="flat", show="*")
        self.password_entry.pack(fill=tk.X, pady=(5, 10), ipady=8)

        # Forgot password link
        forgot_btn = tk.Button(
            right_panel, text="Forgot password?", font=("Calibri", 10, "underline"),
            bg=BG_COLOR, fg=FG_SECONDARY, relief="flat", cursor="hand2",
            command=self.open_forgot_password
        )
        forgot_btn.pack(anchor="e", pady=(0, 15))

        # Login Button
        login_btn = tk.Button(
            right_panel, text="LOG IN", font=("Montserrat", 14, "bold"),
            bg=FG_PRIMARY, fg=BG_COLOR, relief="flat", cursor="hand2",
            command=self.handle_login
        )
        login_btn.pack(fill=tk.X, ipady=10)

        # Sign up link
        nav_frame = tk.Frame(right_panel, bg=BG_COLOR)
        nav_frame.pack(pady=(15, 0))

        tk.Label(nav_frame, text="Don't have an account?",
                 font=("Calibri", 10), bg=BG_COLOR, fg=FG_SECONDARY).pack(side=tk.LEFT)

        signup_btn = tk.Button(
            nav_frame, text="Sign up here", font=("Calibri", 10, "underline"),
            bg=BG_COLOR, fg=FG_PRIMARY, relief="flat", cursor="hand2",
            command=self._build_register_ui
        )
        signup_btn.pack(side=tk.LEFT, padx=5)

    def handle_login(self):
        role = self.current_role.get()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.shake_window()
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        account = VALID_ACCOUNTS.get(role)

        if account and username == account["username"] and password_hash == account["password_hash"]:
            self.show_dashboard(username, role)
        else:
            self.shake_window()
            self.password_entry.delete(0, tk.END)

    # ---------------------------------------------------------
    # FORGOT PASSWORD
    # ---------------------------------------------------------

    def open_forgot_password(self):
        win = tk.Toplevel(self)
        win.title("Forgot Password")
        win.configure(bg=BG_COLOR)
        win.geometry("400x320")
        win.resizable(False, False)
        win.eval('tk::PlaceWindow %s center' % str(win))

        tk.Label(win, text="Reset Password", font=("Calibri", 16, "bold"),
                 bg=BG_COLOR, fg="white").pack(pady=(15, 10))

        # Role
        tk.Label(win, text="ROLE", font=("Calibri", 10, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w", padx=20)
        role_var = tk.StringVar(value=self.current_role.get())
        role_menu = tk.OptionMenu(win, role_var, *ROLES)
        role_menu.config(bg=BG_SECONDARY, fg="white", highlightthickness=0)
        role_menu.pack(fill=tk.X, padx=20, pady=(5, 10))

        # Username
        tk.Label(win, text="USERNAME", font=("Calibri", 12, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w", padx=20)
        username_entry = tk.Entry(win, font=("Calibri", 11),
                                  bg=BG_ENTRY, fg="white",
                                  insertbackground=FG_PRIMARY, relief="flat")
        username_entry.pack(fill=tk.X, padx=20, pady=(5, 10), ipady=5)

        # Email (optional, only checked if exists in account)
        tk.Label(win, text="EMAIL (if required)", font=("Calibri", 12, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w", padx=20)
        email_entry = tk.Entry(win, font=("Calibri", 11),
                               bg=BG_ENTRY, fg="white",
                               insertbackground=FG_PRIMARY, relief="flat")
        email_entry.pack(fill=tk.X, padx=20, pady=(5, 10), ipady=5)

        # New password
        tk.Label(win, text="NEW PASSWORD", font=("Calibri", 12, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w", padx=20)
        new_pw_entry = tk.Entry(win, font=("Calibri", 11),
                                bg=BG_ENTRY, fg="white",
                                insertbackground=FG_PRIMARY, relief="flat", show="*")
        new_pw_entry.pack(fill=tk.X, padx=20, pady=(5, 5), ipady=5)

        # Confirm new password
        tk.Label(win, text="CONFIRM PASSWORD", font=("Calibri", 12, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w", padx=20)
        confirm_pw_entry = tk.Entry(win, font=("Calibri", 11),
                                    bg=BG_ENTRY, fg="white",
                                    insertbackground=FG_PRIMARY, relief="flat", show="*")
        confirm_pw_entry.pack(fill=tk.X, padx=20, pady=(5, 5), ipady=5)

        feedback = tk.Label(win, text="", font=("Calibri", 10),
                            bg=BG_COLOR, fg="#FF6B6B")
        feedback.pack(anchor="w", padx=20, pady=(5, 5))

        def do_reset():
            role = role_var.get()
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            new_pw = new_pw_entry.get()
            confirm_pw = confirm_pw_entry.get()

            if not username or not new_pw or not confirm_pw:
                feedback.config(text="Username and both password fields are required.")
                return

            account = VALID_ACCOUNTS.get(role)
            if not account or account["username"] != username:
                feedback.config(text="No matching account for that role and username.")
                return

            # If account has email stored, require match
            if account.get("email"):
                if not email or email != account["email"]:
                    feedback.config(text="Email does not match this account.")
                    return

            # Password rules
            if len(new_pw) < 8:
                feedback.config(text="Password must be at least 8 characters.")
                return
            if not any(c.isdigit() for c in new_pw):
                feedback.config(text="Password must contain at least one number.")
                return
            if not any(c in "!@#$%^&*()-_=+[]{};:,.<>?/\\|" for c in new_pw):
                feedback.config(text="Password must contain a special character.")
                return
            if new_pw != confirm_pw:
                feedback.config(text="Passwords do not match.")
                return

            # Save new password
            new_hash = hashlib.sha256(new_pw.encode()).hexdigest()
            VALID_ACCOUNTS[role]["password_hash"] = new_hash

            feedback.config(text="Password reset successfully.", fg="#4CFF72")
            win.after(1200, win.destroy)

        reset_btn = tk.Button(
            win, text="Reset Password", font=("Calibri", 12, "bold"),
            bg=FG_PRIMARY, fg=BG_COLOR, relief="flat", cursor="hand2",
            command=do_reset
        )
        reset_btn.pack(fill=tk.X, padx=20, pady=(10, 10), ipady=5)

    # ---------------------------------------------------------
    # REGISTER UI (Role‑Dependent Fields)
    # ---------------------------------------------------------

    def _build_register_ui(self):
        self.clear_container()

        # Left Panel
        left_panel = tk.Frame(self.container, bg="#111111", width=330)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="Formaly", font=("Montserrat", 24, "bold"),
                 bg="#111111", fg=FG_PRIMARY).pack(pady=(25, 10))

        logo_img = tk.PhotoImage(file=r"C:\Users\2rm2j\Documents\Software\Project\Formaly_YR12-SoftwareEngineering-MajorProject\Logo.png")
        tk.Label(left_panel, image=logo_img, bg="#111111").pack()
        left_panel.logo_img = logo_img

        # Right Panel
        right_panel = tk.Frame(self.container, bg=BG_COLOR)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=25, pady=25)

        tk.Label(right_panel, text="CREATE ACCOUNT",
                 font=("Calibri", 18, "bold"), bg=BG_COLOR, fg="white").pack(anchor="w", pady=(5, 15))

        # Role Selector
        tk.Label(right_panel, text="SELECT ROLE", font=("Calibri", 10, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w")

        role_frame = tk.Frame(right_panel, bg=BG_COLOR)
        role_frame.pack(fill=tk.X, pady=(5, 10))

        self.role_buttons = {}
        for role in ROLES:
            btn = tk.Button(
                role_frame, text=role, font=("Calibri", 10),
                bg=BG_SECONDARY if role != self.current_role.get() else FG_PRIMARY,
                fg=FG_SECONDARY if role != self.current_role.get() else BG_COLOR,
                relief="flat", cursor="hand2",
                command=lambda r=role: self.update_register_role(r)
            )
            btn.pack(side=tk.LEFT, padx=4, ipadx=6, ipady=3)
            self.role_buttons[role] = btn

        # Dynamic form container
        self.register_form = tk.Frame(right_panel, bg=BG_COLOR)
        self.register_form.pack(fill=tk.BOTH, expand=True)

        self.build_role_specific_fields()

        # Navigation
        nav_frame = tk.Frame(right_panel, bg=BG_COLOR)
        nav_frame.pack(pady=(10, 0))

        tk.Label(nav_frame, text="Already have an account?",
                 font=("Calibri", 10), bg=BG_COLOR, fg=FG_SECONDARY).pack(side=tk.LEFT)

        login_btn = tk.Button(
            nav_frame, text="Log in", font=("Calibri", 10, "underline"),
            bg=BG_COLOR, fg=FG_PRIMARY, relief="flat", cursor="hand2",
            command=self._build_login_ui
        )
        login_btn.pack(side=tk.LEFT, padx=5)

    def update_register_role(self, role):
        self.current_role.set(role)
        for r, btn in self.role_buttons.items():
            if r == role:
                btn.config(bg=FG_PRIMARY, fg=BG_COLOR)
            else:
                btn.config(bg=BG_SECONDARY, fg=FG_SECONDARY)

        for widget in self.register_form.winfo_children():
            widget.destroy()

        self.build_role_specific_fields()

    def build_role_specific_fields(self):
        role = self.current_role.get()

        # EMAIL (Student + Admin)
        if role in ["Student Planner", "Administrator"]:
            tk.Label(self.register_form, text="EMAIL", font=("Calibri", 14, "bold"),
                     bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w")
            self.reg_email_entry = tk.Entry(self.register_form, font=("Calibri", 12),
                                            bg=BG_ENTRY, fg="white",
                                            insertbackground=FG_PRIMARY, relief="flat")
            self.reg_email_entry.pack(fill=tk.X, pady=(5, 8), ipady=6)
        else:
            self.reg_email_entry = None

        # USERNAME
        tk.Label(self.register_form, text="USERNAME", font=("Calibri", 14, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w")
        self.reg_username_entry = tk.Entry(self.register_form, font=("Calibri", 12),
                                           bg=BG_ENTRY, fg="white",
                                           insertbackground=FG_PRIMARY, relief="flat")
        self.reg_username_entry.pack(fill=tk.X, pady=(5, 8), ipady=6)

        # PASSWORD
        tk.Label(self.register_form, text="PASSWORD", font=("Calibri", 14, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w")

        pw_frame = tk.Frame(self.register_form, bg=BG_COLOR)
        pw_frame.pack(fill=tk.X, pady=(5, 0))

        self.reg_password_entry = tk.Entry(pw_frame, font=("Calibri", 12),
                                           bg=BG_ENTRY, fg="white",
                                           insertbackground=FG_PRIMARY, relief="flat", show="*")
        self.reg_password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)

        pw_toggle = tk.Button(
            pw_frame, text="Show", font=("Calibri", 9),
            bg=BG_SECONDARY, fg="white", relief="flat", cursor="hand2",
            command=lambda: self.toggle_password(self.reg_password_entry, pw_toggle)
        )
        pw_toggle.pack(side=tk.RIGHT, padx=5)

        # Strength Meter
        self.strength_label = tk.Label(self.register_form, text="Strength: Weak",
                                       font=("Calibri", 10),
                                       bg=BG_COLOR, fg="#FF4C4C")
        self.strength_label.pack(anchor="w", pady=(2, 10))

        self.reg_password_entry.bind("<KeyRelease>", self.update_strength_meter)

        # CONFIRM PASSWORD
        tk.Label(self.register_form, text="CONFIRM PASSWORD", font=("Calibri", 14, "bold"),
                 bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w")

        confirm_frame = tk.Frame(self.register_form, bg=BG_COLOR)
        confirm_frame.pack(fill=tk.X, pady=(5, 15))

        self.reg_confirm_entry = tk.Entry(confirm_frame, font=("Calibri", 12),
                                          bg=BG_ENTRY, fg="white",
                                          insertbackground=FG_PRIMARY, relief="flat", show="*")
        self.reg_confirm_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)

        confirm_toggle = tk.Button(
            confirm_frame, text="Show", font=("Calibri", 9),
            bg=BG_SECONDARY, fg="white", relief="flat", cursor="hand2",
            command=lambda: self.toggle_password(self.reg_confirm_entry, confirm_toggle)
        )
        confirm_toggle.pack(side=tk.RIGHT, padx=5)

        # NSW SCHOOL (Admin only)
        if role == "Administrator":
            tk.Label(self.register_form, text="SCHOOL (NSW)", font=("Calibri", 14, "bold"),
                     bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w")

            SCHOOLS_NSW = [
                "Sydney Boys High School",
                "Sydney Girls High School",
                "Parramatta High School",
                "Baulkham Hills High School",
                "Normanhurst Boys High School",
                "James Ruse Agricultural High School",
                "Epping Boys High School",
                "Chatswood High School",
                "Ryde Secondary College"
            ]

            self.school_var = tk.StringVar(value=SCHOOLS_NSW[0])
            school_dropdown = tk.OptionMenu(self.register_form, self.school_var, *SCHOOLS_NSW)
            school_dropdown.config(bg=BG_SECONDARY, fg="white", highlightthickness=0)
            school_dropdown.pack(fill=tk.X, pady=(5, 15))
        else:
            self.school_var = None

        # Feedback label
        self.reg_feedback = tk.Label(self.register_form, text="",
                                     font=("Calibri", 10),
                                     bg=BG_COLOR, fg="#FF6B6B")
        self.reg_feedback.pack(anchor="w", pady=(0, 10))

        # Register Button
        reg_btn = tk.Button(
            self.register_form, text="REGISTER", font=("Montserrat", 13, "bold"),
            bg=FG_PRIMARY, fg=BG_COLOR, relief="flat", cursor="hand2",
            command=self.handle_register
        )
        reg_btn.pack(fill=tk.X, ipady=8)

    # ---------------------------------------------------------
    # REGISTER LOGIC
    # ---------------------------------------------------------

    def handle_register(self):
        role = self.current_role.get()

        email = self.reg_email_entry.get().strip() if self.reg_email_entry else None
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm = self.reg_confirm_entry.get()
        school = self.school_var.get() if self.school_var else None

        # Required fields by role
        if role == "Student Planner":
            if not email or not username or not password or not confirm:
                self.reg_feedback.config(text="All fields are required for Student Planner.")
                self.shake_window()
                return

        elif role == "Support Staff":
            if not username or not password or not confirm:
                self.reg_feedback.config(text="Username and password required for Support Staff.")
                self.shake_window()
                return

        elif role == "Administrator":
            if not email or not username or not password or not confirm or not school:
                self.reg_feedback.config(text="All fields are required for Administrator.")
                self.shake_window()
                return

        # Email validation (only if email exists)
        if email and ("@" not in email or "." not in email):
            self.reg_feedback.config(text="Invalid email format.")
            self.shake_window()
            return

        # Password rules
        if len(password) < 8:
            self.reg_feedback.config(text="Password must be at least 8 characters.")
            self.shake_window()
            return

        if not any(c.isdigit() for c in password):
            self.reg_feedback.config(text="Password must contain at least one number.")
            self.shake_window()
            return

        if not any(c in "!@#$%^&*()-_=+[]{};:,.<>?/\\|" for c in password):
            self.reg_feedback.config(text="Password must contain a special character.")
            self.shake_window()
            return

        if password != confirm:
            self.reg_feedback.config(text="Passwords do not match.")
            self.shake_window()
            return

        # Username uniqueness
        existing = VALID_ACCOUNTS.get(role)
        if existing and existing["username"].lower() == username.lower():
            self.reg_feedback.config(text="Username already exists for this role.")
            self.shake_window()
            return

        # Save account
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        VALID_ACCOUNTS[role] = {
            "username": username,
            "password_hash": password_hash
        }

        if email:
            VALID_ACCOUNTS[role]["email"] = email

        if school:
            VALID_ACCOUNTS[role]["school"] = school

        # Return to login
        self._build_login_ui()
        self.username_entry.insert(0, username)

    # ---------------------------------------------------------
    # DASHBOARD
    # ---------------------------------------------------------

    def show_dashboard(self, username, role):
        self.container.destroy()

        dashboard = tk.Frame(self, bg=BG_COLOR)
        dashboard.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(dashboard, bg="#111111", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text=f"Welcome, {username}", font=("Calibri", 20, "bold"),
                 bg="#111111", fg="white").pack(side=tk.LEFT, padx=20)

        tk.Button(
            header, text="Log Out", font=("Calibri", 16),
            bg=BG_SECONDARY, fg="white", relief="flat", cursor="hand2",
            command=self.logout
        ).pack(side=tk.RIGHT, padx=30)

        content = tk.Frame(dashboard, bg=BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True)
    # ---------------------------------------------------------
    # LOGOUT
    # ---------------------------------------------------------

    def logout(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.container = None
        self.current_role.set(ROLES[0])
        self._build_login_ui()


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":
    app = FormalyApp()
    app.mainloop()