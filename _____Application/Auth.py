import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os

# ---------- DATABASE ----------
def create_user_table():
    conn = sqlite3.connect("Expense_tracker.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---------- AUTH FUNCTION ----------
def handle_auth(action):
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showwarning("Input Error", "Both fields are required.")
        return

    conn = sqlite3.connect("Expense_tracker.db")
    cur = conn.cursor()

    if action == "Register":
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            root.destroy()
            script_path = os.path.join(os.path.dirname(__file__), 'Main.py')
            subprocess.run(["python", script_path, username])
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
    elif action == "Login":
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        if user:
            messagebox.showinfo("Welcome", "Login successful!")
            root.destroy()
            script_path = os.path.join(os.path.dirname(__file__), 'Main.py')
            subprocess.run(["python", script_path, username])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    conn.close()

# ---------- UI SETUP ----------
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("450x480")
root.configure(bg="#ecf0f3")
root.resizable(False, False)

create_user_table()

# ---------- HEADER BAR ----------
header = tk.Frame(root, bg="#2c3e50", height=60)
header.pack(fill="x")
tk.Label(header, text="💸 Expense Tracker", fg="white", bg="#2c3e50", font=("Helvetica", 18, "bold")).pack(pady=10)

# ---------- CARD CONTAINER ----------
card = tk.Frame(root, bg="white", bd=0, relief="flat")
card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=340)

# Title inside card
tk.Label(card, text="Login / Register", font=("Helvetica", 16, "bold"), bg="white", fg="#34495e").pack(pady=(25, 15))

# ---------- USERNAME ----------
tk.Label(card, text="Username", font=("Helvetica", 11), bg="white", anchor="w").pack(fill="x", padx=40)
entry_username = tk.Entry(card, font=("Helvetica", 11), bd=1, relief="solid", bg="#f8f9fa")
entry_username.pack(pady=5, padx=40, fill="x", ipady=6)

# ---------- PASSWORD ----------
tk.Label(card, text="Password", font=("Helvetica", 11), bg="white", anchor="w").pack(fill="x", padx=40, pady=(15, 0))
entry_password = tk.Entry(card, font=("Helvetica", 11), bd=1, relief="solid", show="*", bg="#f8f9fa")
entry_password.pack(pady=5, padx=40, fill="x", ipady=6)

# ---------- BUTTONS ----------
btn_frame = tk.Frame(card, bg="white")
btn_frame.pack(pady=25)

style = {
    "font": ("Helvetica", 11, "bold"),
    "width": 12,
    "bd": 0,
    "activeforeground": "white",
    "cursor": "hand2",
}

btn_login = tk.Button(btn_frame, text="Login", bg="#27ae60", fg="white", activebackground="#1e8449",
                      command=lambda: handle_auth("Login"), **style)
btn_login.grid(row=0, column=0, padx=10)

btn_register = tk.Button(btn_frame, text="Register", bg="#2980b9", fg="white", activebackground="#21618c",
                         command=lambda: handle_auth("Register"), **style)
btn_register.grid(row=0, column=1, padx=10)

# ---------- FOOTER ----------
tk.Label(card, text="Secure your daily expenses", font=("Helvetica", 9), bg="white", fg="#888").pack(pady=(5, 10))

root.mainloop()
