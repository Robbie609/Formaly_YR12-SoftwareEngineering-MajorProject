import tkinter as tk
import hashlib
import time
import sqlite3 as sql
import subprocess
import sys

BG_COLOR="#0B0B0B"
FG_PRIMARY="#FFD24A"
FG_SECONDARY="#C0C0C0"
BG_SECONDARY="#1A1A1A"
BG_ENTRY="#0A0A0A"

ROLES=["Student Planner","Support Staff","Administrator"]

ROLE_MAP={
    "Student Planner":"planner",
    "Support Staff":"helper",
    "Administrator":"admin"
}
DASHBOARD_MAP = {
    "admin": "admin_dashboard.py",
    "planner": "planner_dashboard.py",
    "helper": "support_dashboard.py"
}
class FormalyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Formaly - Login")
        self.geometry("900x600")
        self.configure(bg=BG_COLOR)
        self.resizable(True,True)
        self.eval('tk::PlaceWindow . center')
        self.current_role=tk.StringVar(value=ROLES[0])
        self.container=None
        self.iconphoto(True,tk.PhotoImage(file="Logo.png"))
        self._build_login_ui()

    def clear_container(self):
        if self.container is not None:
            self.container.destroy()
        self.container=tk.Frame(self,bg=BG_COLOR)
        self.container.pack(fill=tk.BOTH,expand=True)

    def select_role(self,role):
        self.current_role.set(role)
        for r,btn in self.role_buttons.items():
            if r==role:
                btn.config(bg=FG_PRIMARY,fg=BG_COLOR)
            else:
                btn.config(bg=BG_SECONDARY,fg=FG_SECONDARY)

    def shake_window(self):
        original_x=self.winfo_x()
        original_y=self.winfo_y()
        offsets=[-20,20,-20,20,-10,10,5]
        for offset in offsets:
            self.geometry(f"+{original_x+offset}+{original_y}")
            self.update()
            time.sleep(0.05)

    def _build_login_ui(self):
        self.clear_container()

        left_panel=tk.Frame(self.container,bg="#111111",width=450)
        left_panel.pack(side=tk.LEFT,fill=tk.Y)
        left_panel.pack_propagate(False)

        tk.Label(
            left_panel,
            text="Formaly",
            font=("Montserrat",26,"bold"),
            bg="#111111",
            fg=FG_PRIMARY
        ).pack(pady=(30,10))

        try:
            logo_img=tk.PhotoImage(file="Logo.png")
            tk.Label(
                left_panel,
                image=logo_img,
                bg="#111111"
            ).pack()
            left_panel.logo_img=logo_img
        except:
            pass

        right_panel=tk.Frame(self.container,bg=BG_COLOR)
        right_panel.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=True,
            padx=40,
            pady=30
        )

        tk.Label(
            right_panel,
            text="WELCOME BACK!",
            font=("Calibri",20,"bold"),
            bg=BG_COLOR,
            fg="white"
        ).pack(anchor="w",pady=(20,20))

        tk.Label(
            right_panel,
            text="SELECT ROLE",
            font=("Calibri",10,"bold"),
            bg=BG_COLOR,
            fg=FG_SECONDARY
        ).pack(anchor="w")

        role_frame=tk.Frame(right_panel,bg=BG_COLOR)
        role_frame.pack(fill=tk.X,pady=(10,15))

        self.role_buttons={}

        for role in ROLES:
            btn=tk.Button(
                role_frame,
                text=role,
                font=("Calibri",10),
                bg=BG_SECONDARY if role!=self.current_role.get() else FG_PRIMARY,
                fg=FG_SECONDARY if role!=self.current_role.get() else BG_COLOR,
                relief="flat",
                cursor="hand2",
                command=lambda r=role:self.select_role(r)
            )

            btn.pack(side=tk.LEFT,padx=5,ipadx=10,ipady=5)
            self.role_buttons[role]=btn

        tk.Label(
            right_panel,
            text="USERNAME",
            font=("Calibri",16,"bold"),
            bg=BG_COLOR,
            fg=FG_SECONDARY,
        ).pack(anchor="w")

        self.username_entry=tk.Entry(
            right_panel,
            font=("Calibri",12),
            bg=BG_ENTRY,
            fg="white",
            insertbackground=FG_PRIMARY,
            relief="flat"
        )

        self.username_entry.pack(fill=tk.X,pady=(5,15),ipady=8)

        tk.Label(
            right_panel,
            text="PASSWORD",
            font=("Calibri",16,"bold"),
            bg=BG_COLOR,
            fg=FG_SECONDARY
        ).pack(anchor="w")

        self.password_entry=tk.Entry(
            right_panel,
            font=("Calibri",12),
            bg=BG_ENTRY,
            fg="white",
            insertbackground=FG_PRIMARY,
            relief="flat",
            show="*"
        )

        self.password_entry.pack(fill=tk.X,pady=(5,15),ipady=8)

        self.feedback_label=tk.Label(
            right_panel,
            text="",
            font=("Calibri",11),
            bg=BG_COLOR,
            fg="#FF6B6B"
        )

        self.feedback_label.pack(anchor="w",pady=(0,10))

        login_btn=tk.Button(
            right_panel,
            text="LOG IN",
            font=("Montserrat",14,"bold"),
            bg=FG_PRIMARY,
            fg=BG_COLOR,
            relief="flat",
            cursor="hand2",
            command=self.handle_login
        )

        login_btn.pack(fill=tk.X,ipady=10)

        forgot_btn=tk.Button(
            right_panel,
            text="Forgot Password?",
            font=("Calibri",10,"underline"),
            bg=BG_COLOR,
            fg=FG_SECONDARY,
            relief="flat",
            cursor="hand2",
            command=lambda:print("Forgot Password Clicked. Haven't implemented yet.")
        )
        forgot_btn.pack(anchor="w",pady=(5,10))

    def handle_login(self):
        username=self.username_entry.get().strip()
        password=self.password_entry.get()
        selected_role=self.current_role.get()

        if not username or not password:
            self.feedback_label.config(text="Please enter all fields.")
            self.shake_window()
            return

        password_hash=hashlib.sha256(password.encode()).hexdigest()
        db_role=ROLE_MAP[selected_role]

        try:
            con=sql.connect("formaly.db")
            cur=con.cursor()

            cur.execute("""
            SELECT Username,Role
            FROM Accounts
            WHERE LOWER(Username)=LOWER(?)
            AND Password_Hashed=?
            AND Role=?
            """,(
                username,
                password_hash,
                db_role
            ))

            account=cur.fetchone()
            con.close()

            if account:
                self.feedback_label.config(text="Login successful!", fg="#4CFF72")
                self.update()
                time.sleep(0.6)
                self.destroy()

                role_key = ROLE_MAP[selected_role]
                dashboard_file = DASHBOARD_MAP.get(role_key)
                
                if dashboard_file:
                    subprocess.Popen([sys.executable, dashboard_file])
                else:
                    print("No dashboard mapped for role:", role_key)

            else:
                self.feedback_label.config(
                    text="Invalid username, password, or role.",
                    fg="#FF6B6B"
                )

                self.password_entry.delete(0,tk.END)
                self.shake_window()

        except Exception as e:
            self.feedback_label.config(
                text=f"Database Error: {e}",
                fg="#FF6B6B"
            )

            self.shake_window()

if __name__=="__main__":
    app=FormalyApp()
    app.mainloop()