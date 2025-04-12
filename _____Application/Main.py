import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
import subprocess
import os


# ---------- DATABASE SETUP ----------
connect = sqlite3.connect("Expense_tracker.db")
cursor = connect.cursor()

# ---------- CREATE TABLE IF NOT EXISTS ----------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Expense_items (
        ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DESCRIPTION TEXT,
        AMOUNT REAL,
        DATE TEXT DEFAULT (datetime('now','localtime'))
    )
""")
connect.commit()


# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Expense Manager")
root.geometry("1000x650")
root.configure(bg="#e9eff6")

# ---------- STYLE CONFIGURATION ----------
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'), background="#3f51b5", foreground="white")
style.configure("Treeview", font=('Segoe UI', 11), rowheight=35, background="#ffffff", fieldbackground="#ffffff")
style.map("Treeview", background=[('selected', '#cddcfa')])

style.configure("TLabel", background="#e9eff6", font=('Segoe UI', 11))
style.configure("TButton", font=('Segoe UI', 11, 'bold'), padding=6)
style.configure("TEntry", font=('Segoe UI', 11), padding=5)


# ---------- MENU ----------
def open_update():
    path = os.path.join(os.path.dirname(__file__), 'Update.py')
    subprocess.run(["python", path])


def open_view():
    path = os.path.join(os.path.dirname(__file__), 'view.py')
    subprocess.run(["python", path])


menubar = tk.Menu(root)
menu_section = tk.Menu(menubar, tearoff=0)
menu_section.add_command(label="Update", command=open_update)
menu_section.add_command(label="View", command=open_view)
menubar.add_cascade(label="Menu", menu=menu_section)
root.config(menu=menubar)


# ---------- HEADER ----------
header_frame = tk.Frame(root, bg="#2c3e50", pady=20)
header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")
tk.Label(header_frame, text="💸 Expense Tracker", font=("Segoe UI", 20, "bold"), fg="white", bg="#2c3e50").pack()


# ---------- SEARCH BAR ----------
style.configure("Rounded.TEntry",
                relief="flat", padding=6, font=("Segoe UI", 11), foreground="black", background="#ffffff")
style.map("TButton", foreground=[('active', 'white')],
          background=[('active', '#388E3C')])

form_frame = tk.Frame(root, bg="#f5f5f5", padx=40, pady=30)
form_frame.grid(row=1, column=0, columnspan=4, padx=20, pady=30, sticky="ew")

# Search Section
search_label = tk.Label(form_frame, text="Search", font=("Segoe UI", 12, 'bold'), bg="#f5f5f5", anchor="w")
search_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 15))

search_entry = ttk.Entry(form_frame, style="Rounded.TEntry", width=35)
search_entry.grid(row=0, column=1, padx=(0, 10), pady=(0, 15))

search_button = tk.Button(form_frame, text="Search", command=lambda: Search_items(),
                          font=("Segoe UI", 11, 'bold'), bg="#388E3C", fg="white", relief="flat", width=10, height=1)
search_button.grid(row=0, column=2, padx=(0, 5), pady=(0, 15))

# ---------- DESCRIPTION, AMOUNT, AND ADD BUTTON ON SAME ROW ----------
desc_label = tk.Label(form_frame, text="Description", font=("Segoe UI", 12, 'bold'), bg="#f5f5f5", anchor="w")
desc_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")

EntryItemDescription = tk.Entry(form_frame, width=30, font=("Segoe UI", 12), relief="solid", bd=1, background="#ffffff")
EntryItemDescription.grid(row=1, column=1, padx=5, pady=10, sticky="w")

amount_label = tk.Label(form_frame, text="Amount", font=("Segoe UI", 12, 'bold'), bg="#f5f5f5", anchor="w")
amount_label.grid(row=1, column=2, padx=5, pady=10, sticky="w")

EntryItemAmount = tk.Entry(form_frame, width=20, font=("Segoe UI", 12), relief="solid", bd=1, background="#ffffff")
EntryItemAmount.grid(row=1, column=3, padx=5, pady=10, sticky="w")

# Add Button on the same row
add_button = tk.Button(form_frame, text="Add Expense", command=lambda: Add_items(),
                       font=("Segoe UI", 12, 'bold'), bg="#2196F3", fg="white", relief="flat", width=20, pady=10)
add_button.grid(row=1, column=4, padx=5, pady=10, sticky="w")


# ---------- TREEVIEW ----------
columns = ("ITEM_ID", "DESCRIPTION", "AMOUNT", "DATE")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=200)

tree.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")


# ---------- FUNCTIONS ----------
def Search_items():
    keyword = search_entry.get()
    if keyword:
        cursor.execute("SELECT * FROM Expense_items WHERE DESCRIPTION LIKE ? OR AMOUNT LIKE ?",
                       ('%' + keyword + '%', '%' + keyword + '%'))
        rows = cursor.fetchall()
        if rows:
            tree.delete(*tree.get_children())  # Clear existing rows
            for row in rows:
                tree.insert("", tk.END, values=(row[0], row[1], f"{row[2]} UGX", row[3]))
        else:
            messagebox.showinfo("Search", "No results found.")
    else:
        messagebox.showwarning("Search", "Enter a keyword to search.")


def Add_items():
    desc = EntryItemDescription.get()
    amt = EntryItemAmount.get()
    if desc and amt:
        try:
            amt = float(amt)
            cursor.execute("INSERT INTO Expense_items (DESCRIPTION, AMOUNT) VALUES (?, ?)", (desc, amt))
            connect.commit()
            EntryItemDescription.delete(0, tk.END)
            EntryItemAmount.delete(0, tk.END)
            messagebox.showinfo("Expense Tracker", "Expense added successfully!")
            show_today_expenses()
        except ValueError:
            messagebox.showwarning("Error", "Amount must be a valid number.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Both Description and Amount are required.")


def show_today_expenses():
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM Expense_items WHERE DATE LIKE ?", (today + '%',))
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())  # Clear previous results
    for row in rows:
        tree.insert("", tk.END, values=(row[0], row[1], f"{row[2]} UGX", row[3]))


# ---------- RESPONSIVENESS ----------
root.grid_rowconfigure(3, weight=1)
for col in range(5):
    root.grid_columnconfigure(col, weight=1)

# ---------- INITIALIZE ----------
show_today_expenses()

# ---------- RUN ----------
root.mainloop()
connect.close()
