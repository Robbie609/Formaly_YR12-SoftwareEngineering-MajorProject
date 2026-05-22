import sqlite3
import hashlib

# Connect to database
con = sqlite3.connect("formaly.db")
cur = con.cursor()

# Password
password = "EppingFormal26ADMIN"

# Hash password
password_hashed = hashlib.sha256(password.encode()).hexdigest()

# Insert new admin account
cur.execute("""
INSERT INTO Accounts
(Username, Password_Hashed, School, Formal_Name, Role)
VALUES (?, ?, ?, ?, ?)
""", (
    "Calvin",
    password_hashed,
    "Epping Boys High School",
    "EppingFormal2026",
    "admin"
))

con.commit()

print("Calvin admin account created successfully!")

con.close()