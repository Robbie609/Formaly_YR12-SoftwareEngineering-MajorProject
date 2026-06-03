import tkinter as tk
from tkinter import messagebox

from database.formaly_database_manager import get_user
from utils.styles import *
from utils.helpers import center_window
from utils.validators import validate_login


class FormalyLoginApp(tk.Tk):
    def __init__(self, parent=None):
        super().__init__()

        self.title("Formaly - Login")
        self.configure(bg=BG)
        self.geometry("1200x700")
        self.resizable(True, True)

        center_window(self, 1200, 700)

        self.current_user = None
        self.selected_role = None
        self.parent = parent
        self.build_ui()

    def build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        left = tk.Frame(self, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)
        left.rowconfigure(1, weight=0)

        logo_container = tk.Frame(left, bg=BG)
        logo_container.grid(row=0, column=0, sticky="nsew")
        logo_container.columnconfigure(0, weight=1)
        logo_container.rowconfigure(0, weight=1)

        logo_circle = tk.Frame(logo_container, bg=BG, width=365, height=315)
        logo_circle.grid(row=0, column=0)
        logo_circle.pack_propagate(False)

        logo_image = tk.PhotoImage(file="assets/logo.png")
        logo_label = tk.Label(logo_circle, image=logo_image, bg=BG)
        logo_label.image = logo_image
        logo_label.pack(expand=True)

        branding = tk.Frame(left, bg=BG)
        branding.grid(row=1, column=0, sticky="ew", pady=30)

        tk.Label(
            branding,
            text="FORMALY",
            bg=BG,
            fg="white",
            font=TITLE
        ).pack(anchor="center")

        tk.Label(
            branding,
            text="Formal Management System",
            bg=BG,
            fg=SECONDARY,
            font=SMALL
        ).pack(anchor="center", pady=3)

    def build_right_panel(self):
        right = tk.Frame(self, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=50, pady=50)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        card = tk.Frame(right, bg=CARD, relief="solid", borderwidth=1)
        card.grid(row=0, column=0, sticky="nsew")
        card.columnconfigure(0, weight=1)

        content = tk.Frame(card, bg=CARD)
        content.pack(fill="both", expand=True, padx=35, pady=28)

        tk.Label(
            content,
            text="Welcome Back",
            bg=CARD,
            fg="white",
            font=TITLE
        ).pack(anchor="w", pady=(0, 2))

        tk.Label(
            content,
            text="Sign in to continue",
            bg=CARD,
            fg=SECONDARY,
            font=FONT
        ).pack(anchor="w", pady=(0, 18))

        tk.Label(
            content,
            text="Select Role",
            bg=CARD,
            fg="white",
            font=FONT_BOLD
        ).pack(anchor="w", pady=(0, 9))

        role_frame = tk.Frame(content, bg=CARD)
        role_frame.pack(anchor="w", pady=(0, 18))

        self.role_buttons = {}
        for role in ["Admin", "Planner", "Support"]:
            btn = tk.Button(
                role_frame,
                text=role,
                bg=ENTRY,
                fg=SECONDARY,
                font=FONT,
                border=1,
                relief="solid",
                cursor="hand2",
                command=lambda r=role: self.select_role(r),
                padx=14,
                pady=7
            )
            btn.pack(side="left", padx=(0, 9))
            self.role_buttons[role] = btn

        tk.Label(
            content,
            text="Username",
            bg=CARD,
            fg="white",
            font=FONT_BOLD
        ).pack(anchor="w", pady=(0, 7))

        self.username_entry = tk.Entry(
            content,
            bg=ENTRY,
            fg="white",
            font=FONT,
            border=1,
            relief="solid",
            insertbackground="white"
        )
        self.username_entry.pack(fill="x", pady=(0, 14), ipady=9)
        self.username_entry.bind("<FocusIn>", self.on_focus_in)
        self.username_entry.bind("<FocusOut>", self.on_focus_out)

        tk.Label(
            content,
            text="Password",
            bg=CARD,
            fg="white",
            font=FONT_BOLD
        ).pack(anchor="w", pady=(0, 7))

        self.password_entry = tk.Entry(
            content,
            bg=ENTRY,
            fg="white",
            font=FONT,
            show="●",
            border=1,
            relief="solid",
            insertbackground="white"
        )
        self.password_entry.pack(fill="x", pady=(0, 18), ipady=12)
        self.password_entry.bind("<FocusIn>", self.on_focus_in)
        self.password_entry.bind("<FocusOut>", self.on_focus_out)
        self.password_entry.bind("<Return>", lambda e: self.login())

        self.login_btn = tk.Button(
            content,
            text="Sign In",
            bg=PRIMARY,
            fg="black",
            font=FONT_BOLD,
            command=self.login,
            activebackground="#FFE066",
            activeforeground="black",
            border=0,
            cursor="hand2"
        )
        self.login_btn.pack(fill="x", pady=(0, 11), ipady=9)

        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#FFE066"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg=PRIMARY))

        link_frame = tk.Frame(content, bg=CARD)
        link_frame.pack(anchor="center", pady=(0, 11))

        tk.Label(link_frame, text="Don't have an account? ", bg=CARD, fg=SECONDARY, font=FONT).pack(side="left")

        register_link = tk.Label(
            link_frame,
            text="Register",
            bg=CARD,
            fg=PRIMARY,
            font=FONT_BOLD,
            cursor="hand2"
        )
        register_link.pack(side="left")
        register_link.bind("<Button-1>", lambda e: self.open_register())

        self.status_label = tk.Label(
            content,
            text="",
            bg=CARD,
            fg=ERROR,
            font=SMALL,
            wraplength=280
        )
        self.status_label.pack(anchor="w", pady=(0, 0))

    def on_focus_in(self, event):
        widget = event.widget
        if isinstance(widget, tk.Entry):
            widget.config(relief="solid", borderwidth=2)

    def on_focus_out(self, event):
        widget = event.widget
        if isinstance(widget, tk.Entry):
            widget.config(relief="solid", borderwidth=1)

    def select_role(self, role):
        self.selected_role = role
        for btn_role, btn in self.role_buttons.items():
            if btn_role == role:
                btn.config(bg=PRIMARY, fg="black")
            else:
                btn.config(bg=ENTRY, fg=SECONDARY)

    def login(self):
        if not self.selected_role:
            self.show_status("Please select a role.", ERROR)
            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        valid, msg = validate_login(username, password)
        if not valid:
            self.show_status(msg, ERROR)
            return

        try:
            user = get_user(username, password)

            if not user:
                self.show_status("Invalid username or password.", ERROR)
                return

            user_role = user[5].strip().lower()

            if user_role != self.selected_role.lower():
                self.show_status("This account is not authorized for the selected role.", ERROR)
                return

            self.current_user = user
            self.show_status("Login successful!", SUCCESS)
            self.after(500, lambda: self.open_dashboard(user_role))

        except Exception as e:
            self.show_status(f"Error: {str(e)}", ERROR)

    def open_dashboard(self, role):
        try:
            if role == "admin":
                from pages.admin.admin_dashboard import AdminDashboard
                dashboard = AdminDashboard(self.current_user)
            elif role == "planner":
                from pages.planner.planner_dashboard import PlannerDashboard
                dashboard = PlannerDashboard(self.current_user)
            elif role in ["support", "helper"]:
                from pages.support.support_dashboard import SupportDashboard
                dashboard = SupportDashboard(self.current_user)
            else:
                self.show_status(f"Unknown role: {role}", ERROR)
                return

            self.destroy()
            dashboard.mainloop()

        except Exception as e:
            self.show_status(f"Error: {str(e)}", ERROR)

    def open_register(self):
        try:
            from pages.attendee.attendee_dashboard import FormalInvitationPage
            register = FormalInvitationPage(self)
            self.withdraw()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open register page: {str(e)}")

    def show_status(self, message, color):
        self.status_label.config(text=message, fg=color)
        if color == SUCCESS:
            self.after(2000, lambda: self.status_label.config(text=""))
