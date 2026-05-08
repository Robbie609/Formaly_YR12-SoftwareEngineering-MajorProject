from tkinter import PhotoImage
import tkinter as tk
from email.mime import image
import tkinter as tk
from tkinter import messagebox
import hashlib
import time

# --- Configuration & Mock Data ---
BG_COLOR = "#0B0B0B"
FG_PRIMARY = "#FFD24A"
FG_SECONDARY = "#C0C0C0"
BG_SECONDARY = "#1A1A1A"
BG_ENTRY = "#0A0A0A"

ROLES = ["Student Planner", "Support Staff", "Administrator"]

# Passwords hashed with SHA-256 for 'ebhs111'
PASSWORD_HASH = hashlib.sha256("EBHS".encode()).hexdigest()

VALID_ACCOUNTS = {
    "Student Planner": {"username": "Rowan", "password_hash": PASSWORD_HASH},
    "Support Staff": {"username": "Rigved", "password_hash": PASSWORD_HASH},
    "Administrator": {"username": "Schadel", "password_hash": PASSWORD_HASH}
}

PERMISSIONS = {
    "Student Planner": {
        "View Records": True, "Create Records": False, "Edit Records": False,
        "Delete Records": False, "Finalise": False, "Send Invites": False
    },
    "Support Staff": {
        "View Records": True, "Create Records": True, "Edit Records": True,
        "Delete Records": False, "Finalise": False, "Send Invites": True
    },
    "Administrator": {
        "View Records": True, "Create Records": True, "Edit Records": True,
        "Delete Records": True, "Finalise": True, "Send Invites": True
    }
}

class FormalyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Formaly - Login")
        self.geometry("900x600")
        self.configure(bg=BG_COLOR)
        self.resizable(True, True)
        
        # Center window
        self.eval('tk::PlaceWindow . center')
        
        self.current_role = tk.StringVar(value=ROLES[0])
        
        self._build_login_ui()
        
    def _build_login_ui(self):
        # Container
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Left Panel (Branding)
        left_panel = tk.Frame(self.container, bg="#111111", width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)
        
        # Right Panel (Form)
        right_panel = tk.Frame(self.container, bg=BG_COLOR)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Branding Content
        tk.Label(left_panel, text="Formaly", font=("Montserrat", 28, "bold"), bg="#111111", fg=FG_PRIMARY).pack(pady=(36, 10))
        logo_img = PhotoImage(file=r"C:\Users\2rm2j\Documents\Software\Project\Formaly_YR12-SoftwareEngineering-MajorProject\Logo.png")
        tk.Label(left_panel, image=logo_img, bg="#111111").pack()

# Keep a reference so Python doesn't garbage-collect the image
        left_panel.logo_img = logo_img
        # Form Content
        tk.Label(right_panel, text="WELCOME BACK!", font=("Calibri", 20, "bold"), bg=BG_COLOR, fg="white").pack(anchor="w", pady=(20, 20))
        
        # Role Selector
        tk.Label(right_panel, text="SELECT ROLE", font=("Calibri", 10, "bold"), bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w")
        
        role_frame = tk.Frame(right_panel, bg=BG_COLOR)
        role_frame.pack(fill=tk.X, pady=(10, 15))
        
        self.role_buttons = {}
        for role in ROLES:
            btn = tk.Button(
                role_frame, text=role, font=("Calibri", 10), 
                bg=BG_SECONDARY if role != self.current_role.get() else FG_PRIMARY, 
                fg=FG_SECONDARY if role != self.current_role.get() else BG_COLOR,
                relief="flat", cursor="hand2", command=lambda r=role: self.select_role(r)
            )
            btn.pack(side=tk.LEFT, padx=(0, 10), ipadx=10, ipady=5)
            self.role_buttons[role] = btn
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn, r=role: self.on_btn_hover(b, r))
            btn.bind("<Leave>", lambda e, b=btn, r=role: self.on_btn_leave(b, r))
            
# Username
        tk.Label(right_panel, text="USERNAME", font=("Calibri", 16, "bold"), bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="nw")
        self.username_entry = tk.Entry(right_panel, font=("Calibri", 12), bg=BG_ENTRY, fg="white", insertbackground=FG_PRIMARY, relief="flat")
        self.username_entry.pack(fill=tk.X, pady=(5, 15), ipadx=100, ipady=8)
        self.username_entry.bind("<FocusIn>", lambda e: self.on_focus(self.username_entry))
        self.username_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.username_entry))

        # Password
        tk.Label(right_panel, text="PASSWORD", font=("Calibri", 16, "bold"), bg=BG_COLOR, fg=FG_SECONDARY).pack(anchor="w")
        self.password_entry = tk.Entry(right_panel, font=("Calibri", 12), bg=BG_ENTRY, fg="white", insertbackground=FG_PRIMARY, relief="flat", show="**")
        self.password_entry.pack(fill=tk.X, pady=(5, 25), ipady=8)
        self.password_entry.bind("<FocusIn>", lambda e: self.on_focus(self.password_entry))
        self.password_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.password_entry))
        
        # Login Button
        self.login_btn = tk.Button(
            right_panel, text="LOG IN", font=("Montserrat", 14, "bold"),
            bg=FG_PRIMARY, fg=BG_COLOR, relief="flat", cursor="hand2", command=self.handle_login
        )
        self.login_btn.pack(fill=tk.X, ipady=10)
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#e5bc42"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg=FG_PRIMARY))
        
        # Style entries
        self.on_focus_out(self.username_entry)
        self.on_focus_out(self.password_entry)

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
            
    def show_dashboard(self, username, role):
        self.container.destroy()
        
        dashboard = tk.Frame(self, bg=BG_COLOR)
        dashboard.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(dashboard, bg="#111111", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text=f"Welcome, {username}", font=("Calibri", 18, "bold"), bg="#111111", fg="white").pack(side=tk.LEFT, padx=30)
        tk.Label(header, text=f"{role} Portal", font=("Calibri", 12), bg="#111111", fg=FG_PRIMARY).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            header, text="Log Out", font=("Calibri", 10), bg=BG_SECONDARY, fg="white", 
            relief="flat", cursor="hand2", command=self.logout
        ).pack(side=tk.RIGHT, padx=30)

    def logout(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._build_login_ui()

if __name__ == "__main__":
    app = FormalyApp()
    app.mainloop()