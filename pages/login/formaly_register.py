import tkinter as tk
from utils.styles import *
from utils.helpers import center_window


class FormalyRegisterApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Formaly - Register")
        self.configure(bg=BG)
        self.geometry("1200x700")
        self.resizable(True, True)

        self.parent = parent
        center_window(self, 1200, 700)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
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

        logo_container = tk.Frame(left, bg=BG)
        logo_container.grid(row=0, column=0, sticky="nsew")

        logo_circle = tk.Frame(logo_container, bg=BG, width=360, height=300)
        logo_circle.pack_propagate(False)
        logo_circle.pack(expand=True)

        logo_image = tk.PhotoImage(file="assets/logo.png")
        logo_label = tk.Label(logo_circle, image=logo_image, bg=BG)
        logo_label.image = logo_image
        logo_label.pack(expand=True)

        branding = tk.Frame(left, bg=BG)
        branding.grid(row=1, column=0, pady=20)

        tk.Label(
            branding,
            text="FORMALY",
            bg=BG,
            fg="white",
            font=TITLE
        ).pack()

        tk.Label(
            branding,
            text="Formaly Management System",
            bg=BG,
            fg=SECONDARY,
            font=SMALL
        ).pack(pady=3)

    def build_right_panel(self):
        right = tk.Frame(self, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)

        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        card = tk.Frame(right, bg=CARD, relief="solid", borderwidth=1)
        card.grid(row=0, column=0, sticky="nsew")

        # INNER CONTENT (NO CANVAS — FIXES WIDTH ISSUE)
        content = tk.Frame(card, bg=CARD)
        content.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(
            content,
            text="Create Account",
            bg=CARD,
            fg="white",
            font=TITLE
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Join Formaly today",
            bg=CARD,
            fg=SECONDARY,
            font=FONT
        ).pack(anchor="w", pady=(0, 5))

        self.create_field(content, "Formal Name", "formal_name")
        self.create_field(content, "Email", "email")
        self.create_field(content, "School", "school")
        self.create_field(content, "Username", "username")
        self.create_field(content, "Password", "password", show="●")

        btn = tk.Button(
            content,
            text="Create Account",
            bg=PRIMARY,
            fg="black",
            font=FONT_BOLD,
            activebackground="#FFE066",
            activeforeground="black",
            border=0,
            cursor="hand2"
        )
        btn.pack(fill="x", pady=(15, 20), ipady=8)

        btn.bind("<Enter>", lambda e: btn.config(bg="#FFE066"))
        btn.bind("<Leave>", lambda e: btn.config(bg=PRIMARY))

        link_frame = tk.Frame(content, bg=CARD)
        link_frame.pack()

        tk.Label(
            link_frame,
            text="Already have an account? ",
            bg=CARD,
            fg=SECONDARY,
            font=FONT
        ).pack(side="left")

        login_link = tk.Label(
            link_frame,
            text="Login",
            bg=CARD,
            fg=PRIMARY,
            font=FONT_BOLD,
            cursor="hand2"
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.go_back())

    def create_field(self, parent, label, field_name, show=None):
        tk.Label(
            parent,
            text=label,
            bg=CARD,
            fg="white",
            font=FONT_BOLD
        ).pack(anchor="w", pady=(10, 5))

        entry = tk.Entry(
            parent,
            bg=ENTRY,
            fg="white",
            font=FONT,
            insertbackground="white",
            show=show,
            relief="solid",
            borderwidth=1
        )
        entry.pack(fill="x", ipady=8)

        entry.bind("<FocusIn>", lambda e: e.widget.config(borderwidth=2))
        entry.bind("<FocusOut>", lambda e: e.widget.config(borderwidth=2))

        setattr(self, f"{field_name}_entry", entry)

    def go_back(self):
        self.destroy()
        self.parent.deiconify()

    def on_close(self):
        self.go_back()