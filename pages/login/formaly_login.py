import tkinter as tk
from tkinter import messagebox

from database.formaly_database_manager import get_user
from utils.styles import *
from utils.helpers import center_window
from utils.validators import validate_login


class FormalyLoginApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Formaly - Login")
        self.configure(bg=BG)
        self.geometry("1200x600")
        self.resizable(True, True)

        center_window(self, 1200, 600)

        self.current_user = None
        self.build_ui()

    def build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        left = tk.Frame(self, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)
        left.rowconfigure(1, weight=0)

        logo_container = tk.Frame(left, bg=BG)
        logo_container.grid(row=0, column=0, sticky="nsew")
        logo_container.columnconfigure(0, weight=1)
        logo_container.rowconfigure(0, weight=1)

        logo_circle = tk.Frame(logo_container, bg=BG, width=356, height=315)
        logo_circle.grid(row=0, column=0)
        logo_circle.pack_propagate(False)

        logo_image = tk.PhotoImage(file="assets/logo.png")
        logo_image = logo_image.subsample(1, 1)
        logo_label = tk.Label(logo_circle, image=logo_image, bg=BG)
        logo_label.image = logo_image
        logo_label.pack(expand=True)

        branding = tk.Frame(left, bg=BG)
        branding.grid(row=1, column=0, sticky="ew", pady=20)

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
        ).pack(anchor="center", pady=5)

    def build_right_panel(self):
        right = tk.Frame(self, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        card = tk.Frame(right, bg=CARD, relief="solid", borderwidth=1)
        card.grid(row=0, column=0, sticky="nsew")
        card.columnconfigure(0, weight=1)

        padding = tk.Frame(card, bg=CARD)
        padding.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            padding,
            text="Welcome Back",
            bg=CARD,
            fg="white",
            font=TITLE
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            padding,
            text="Sign in to continue",
            bg=CARD,
            fg=SECONDARY,
            font=FONT
        ).pack(anchor="w", pady=(0, 25))

        tk.Label(
            padding,
            text="Username",
            bg=CARD,
            fg="white",
            font=FONT_BOLD
        ).pack(anchor="w", pady=(0, 8))

        self.username_entry = tk.Entry(
            padding,
            bg=ENTRY,
            fg="white",
            font=FONT,
            border=1,
            relief="solid",
            insertbackground="white"
        )
        self.username_entry.pack(fill="x", pady=(0, 15), ipady=10)
        self.username_entry.bind("<FocusIn>", self.on_focus_in)
        self.username_entry.bind("<FocusOut>", self.on_focus_out)

        tk.Label(
            padding,
            text="Password",
            bg=CARD,
            fg="white",
            font=FONT_BOLD
        ).pack(anchor="w", pady=(0, 8))

        self.password_entry = tk.Entry(
            padding,
            bg=ENTRY,
            fg="white",
            font=FONT,
            show="●",
            border=1,
            relief="solid",
            insertbackground="white"
        )
        self.password_entry.pack(fill="x", pady=(0, 20), ipady=10)
        self.password_entry.bind("<FocusIn>", self.on_focus_in)
        self.password_entry.bind("<FocusOut>", self.on_focus_out)
        self.password_entry.bind("<Return>", lambda e: self.login())

        self.login_btn = tk.Button(
            padding,
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
        self.login_btn.pack(fill="x", pady=(0, 15), ipady=10)

        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#FFE066"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg=PRIMARY))

        self.status_label = tk.Label(
            padding,
            text="",
            bg=CARD,
            fg=ERROR,
            font=SMALL,
            wraplength=280
        )
        self.status_label.pack(anchor="w", pady=(10, 0))

    def on_focus_in(self, event):
        widget = event.widget
        if isinstance(widget, tk.Entry):
            widget.config(relief="solid", borderwidth=2)

    def on_focus_out(self, event):
        widget = event.widget
        if isinstance(widget, tk.Entry):
            widget.config(relief="solid", borderwidth=1)

    def login(self):
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

            self.current_user = user
            role = user[3]

            self.show_status("Login successful!", SUCCESS)
            self.after(500, lambda: self.open_dashboard(role))

        except Exception as e:
            self.show_status(f"Error: {str(e)}", ERROR)

    def open_dashboard(self, role):
        try:
            if role == "Admin":
                from pages.admin.admin_dashboard import AdminDashboard
                dashboard = AdminDashboard()
            elif role == "Attendee":
                try:
                    from pages.attendee.attendee_dashboard import AttendeeDashboard
                    dashboard = AttendeeDashboard()
                except:
                    messagebox.showinfo("Info", "Attendee dashboard is under development.")
                    return
            elif role == "Planner":
                try:
                    from pages.planner.planner_dashboard import PlannerDashboard
                    dashboard = PlannerDashboard()
                except:
                    messagebox.showinfo("Info", "Planner dashboard is under development.")
                    return
            elif role == "Support":
                try:
                    from pages.support.support_dashboard import SupportDashboard
                    dashboard = SupportDashboard()
                except:
                    messagebox.showinfo("Info", "Support dashboard is under development.")
                    return
            else:
                self.show_status(f"Unknown role: {role}", ERROR)
                return

            self.destroy()
            dashboard.mainloop()

        except Exception as e:
            self.show_status(f"Error: {str(e)}", ERROR)

    def show_status(self, message, color):
        self.status_label.config(text=message, fg=color)
        if color == SUCCESS:
            self.after(2000, lambda: self.status_label.config(text=""))
