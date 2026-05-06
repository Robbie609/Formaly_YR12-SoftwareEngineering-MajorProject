import tkinter as tk
from tkinter import ttk

# ---------- THEME ----------

BG = "#0B0B0B"
FG = "#FFD24A"
PRIMARY = "#FFD24A"
SECONDARY = "#C0C0C0"

# ---------- ROLES & PERMISSIONS ----------

ROLES = {
    "Student Planner": {
        "create": True,
        "edit": True,
        "view": True,
        "delete": False,
        "finalise": False,
        "send_invites": False,
    },
    "Support Staff": {
        "create": False,
        "edit": True,
        "view": True,
        "delete": False,
        "finalise": False,
        "send_invites": True,
    },
    "Administrator": {
        "create": True,
        "edit": True,
        "view": True,
        "delete": True,
        "finalise": True,
        "send_invites": True,
    },
}

# ----------- LOG IN WINDOW -----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Formaly - Log In")
        self.geometry("400x300")
        self.configure(bg=BG)

        # Username
        self.username_label = tk.Label(self, text="Username:", bg=BG, fg=FG)
        self.username_label.pack(pady=(30, 5))
        self.username_entry = tk.Entry(self, bg=SECONDARY, fg=BG)
        self.username_entry.pack(pady=5)

        # Password
        self.password_label = tk.Label(self, text="Password:", bg=BG, fg=FG)
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", bg=SECONDARY, fg=BG)
        self.password_entry.pack(pady=5)

        # Log In Button
        self.login_button = tk.Button(
            self,
            text="Log In",
            bg=PRIMARY,
            fg=BG,
            command=self.login,
            width=10,
            height=2,
        )
        self.login_button.pack(pady=(20, 10))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Placeholder for authentication logic
        print(f"Attempting to log in with Username: {username} and Password: {password}")
    
    def create_account(self):
        # Placeholder for account creation logic
        print("Redirecting to account creation page...")
    
    def forgot_password(self):
        # Placeholder for password recovery logic
        print("Redirecting to password recovery page...")

    def exit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
