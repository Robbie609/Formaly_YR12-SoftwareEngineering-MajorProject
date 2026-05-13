import tkinter as tk
import hashlib

app = tk.Tk()
app.title("Formaly")
app.geometry("900x600")

BG="#0B0B0B"
FG="#FFD24A"

app.configure(bg=BG)
password_hash = hashlib.sha256("password".encode()).hexdigest()
VALID_ACCOUNTS = {
    "admin": password_hash
}
tk.Label(app, text="username").pack()
username = tk.Entry(app)
username.pack()

tk.Label(app, text="password").pack()
password = tk.Entry(app, show="*")
password.pack()

def login():
    if username.get() == "admin":
        print("Success")
    else:
        print("Fail")

tk.Button(app, text="Login", bg=BG, fg=FG, command=login).pack()

app.mainloop()