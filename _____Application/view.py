import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

# ---------- DATABASE SETUP ----------
connect = sqlite3.connect("Expense_tracker.db")
cursor = connect.cursor()
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("950x600")
root.configure(bg="#f0f2f5")

# ---------- FUNCTIONS ----------
def open_update():
    script_path = os.path.join(os.path.dirname(__file__), 'Update.py')
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
  
def open_Main():
    script_path = os.path.join(os.path.dirname(__file__), 'Main.py')
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
  
menubar = tk.Menu(root)
forms_menu = tk.Menu(menubar, tearoff=0)
forms_menu.add_command(label="Update", command=open_update)
forms_menu.add_command(label="Main", command=open_Main)
menubar.add_cascade(label="Menu", menu=forms_menu)
root.config(menu=menubar)
def Refresh_items(sort_by="DATE", sort_order="ASC"):
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute(f"SELECT * FROM Expense_items ORDER BY {sort_by} {sort_order}")
    rows = cursor.fetchall()
    for row in rows:
        row = list(row)
        row[2] = f"{row[2]} UGX"
        tree.insert("", tk.END, values=row)

def on_sort():
    sort_column = sort_column_var.get()
    sort_direction = sort_direction_var.get()
    Refresh_items(sort_column, sort_direction)


# ---------- GUI SETUP ----------


style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#4e73df", foreground="white")
style.configure("Treeview", font=('Arial', 10), rowheight=30, background="#ffffff", fieldbackground="#ffffff")
style.map("Treeview", background=[('selected', '#d1e0ff')])
style.configure("TLabel", background="#f0f2f5", font=('Arial', 10))
style.configure("TButton", font=('Arial', 10, 'bold'), padding=6)
style.configure("TEntry", padding=5)

# ---------- Top Sort Frame ----------
sort_frame = ttk.Frame(root, padding=10)
sort_frame.pack(fill=tk.X)

ttk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT, padx=5)
sort_column_var = tk.StringVar(value="DATE")
sort_column_menu = ttk.Combobox(sort_frame, textvariable=sort_column_var, values=["DESCRIPTION", "AMOUNT", "DATE"], width=15, state="readonly")
sort_column_menu.pack(side=tk.LEFT, padx=5)

ttk.Label(sort_frame, text="Direction:").pack(side=tk.LEFT, padx=5)
sort_direction_var = tk.StringVar(value="ASC")
sort_direction_menu = ttk.Combobox(sort_frame, textvariable=sort_direction_var, values=["ASC", "DESC"], width=10, state="readonly")
sort_direction_menu.pack(side=tk.LEFT, padx=5)

ttk.Button(sort_frame, text="Apply Sort", command=on_sort).pack(side=tk.LEFT, padx=10)

# ---------- Treeview Frame ----------
tree_frame = tk.Frame(root, bg="#ffffff", highlightbackground="#dcdcdc", highlightthickness=1)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

columns = ("ITEM_ID", "DESCRIPTION", "AMOUNT", "DATE")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=150)

tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>")



def styled_btn(master, text, command, color):
    return tk.Button(master, text=text, command=command,
                     font=('Arial', 10, 'bold'), bg=color, fg='white',
                     activebackground='#333333', relief='flat', padx=15, pady=8)

# ---------- Launch ----------
Refresh_items()
root.mainloop()

