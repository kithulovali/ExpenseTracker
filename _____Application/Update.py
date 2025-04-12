import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import subprocess

# ---------- DATABASE SETUP ----------
connect = sqlite3.connect("Expense_tracker.db")
cursor = connect.cursor()
root = tk.Tk()
root.title("Main Window")
root.geometry("950x600")
root.configure(bg="#f0f2f5")
# ---------- FUNCTION TO REFRESH ITEMS ----------
def open_Main():
    script_path = os.path.join(os.path.dirname(__file__), 'Main.py')
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
  
def open_view():
    script_path = os.path.join(os.path.dirname(__file__), 'view.py')
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
  
menubar = tk.Menu(root)
forms_menu = tk.Menu(menubar, tearoff=0)
forms_menu.add_command(label="Main", command=open_Main)
forms_menu.add_command(label="View", command=open_view)
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

def Add_items():
    desc = EntryItemDescription.get()
    amount = EntryItemAmount.get()
    if desc and amount:
        try:
            amount = float(amount)
            cursor.execute("INSERT INTO Expense_items (DESCRIPTION, AMOUNT) VALUES (?, ?)", (desc, amount))
            connect.commit()
            EntryItemDescription.delete(0, tk.END)
            EntryItemAmount.delete(0, tk.END)
            Refresh_items()
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showwarning("Invalid", "Amount must be a valid number.")
    else:
        messagebox.showwarning("Missing", "Please fill all fields")

def Update_item():
    selected = tree.selection()
    if selected:
        item_id = tree.item(selected)["values"][0]
        desc = EntryItemDescription.get()
        amount = EntryItemAmount.get()
        if desc and amount:
            try:
                amount = float(amount)
                cursor.execute("UPDATE Expense_items SET DESCRIPTION = ?, AMOUNT = ? WHERE ITEM_ID = ?",
                               (desc, amount, item_id))
                connect.commit()
                Refresh_items()
                messagebox.showinfo("Updated", "Expense updated successfully!")
            except ValueError:
                messagebox.showwarning("Invalid", "Amount must be a valid number.")
        else:
            messagebox.showwarning("Missing", "Please fill all fields")
    else:
        messagebox.showwarning("No Selection", "Please select an item to update.")

def Delete_item():
    selected = tree.selection()
    if selected:
        item_id = tree.item(selected)["values"][0]
        cursor.execute("DELETE FROM Expense_items WHERE ITEM_ID = ?", (item_id,))
        connect.commit()
        Refresh_items()
        messagebox.showinfo("Deleted", "Expense deleted successfully!")
    else:
        messagebox.showwarning("No Selection", "Please select an item to delete.")

def on_tree_select(event):
    selected = tree.selection()
    if selected:
        item = tree.item(selected)["values"]
        EntryItemDescription.delete(0, tk.END)
        EntryItemDescription.insert(0, item[1])
        EntryItemAmount.delete(0, tk.END)
        EntryItemAmount.insert(0, item[2].replace(" UGX", ""))

# ---------- MAIN WINDOW SETUP ----------


style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#4e73df", foreground="white")
style.configure("Treeview", font=('Arial', 10), rowheight=30, background="#ffffff", fieldbackground="#ffffff")
style.map("Treeview", background=[('selected', '#d1e0ff')])
style.configure("TLabel", background="#f0f2f5", font=('Arial', 10))
style.configure("TButton", font=('Arial', 10, 'bold'), padding=6)
style.configure("TEntry", padding=5)

# ---------- TOP SORT FRAME ----------
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

# ---------- TREEVIEW FRAME ----------
tree_frame = tk.Frame(root, bg="#ffffff", highlightbackground="#dcdcdc", highlightthickness=1)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

columns = ("ITEM_ID", "DESCRIPTION", "AMOUNT", "DATE")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=150)

tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", on_tree_select)

# ---------- FORM FRAME ----------
form_frame = ttk.Frame(root, padding=20)
form_frame.pack(fill=tk.X, padx=20)

ttk.Label(form_frame, text="Description:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
EntryItemDescription = ttk.Entry(form_frame, width=40)
EntryItemDescription.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(form_frame, text="Amount (UGX):").grid(row=0, column=2, padx=10, pady=10, sticky=tk.E)
EntryItemAmount = ttk.Entry(form_frame, width=20)
EntryItemAmount.grid(row=0, column=3, padx=10, pady=10)

# ---------- ACTION BUTTONS FRAME ----------
btn_frame = tk.Frame(root, bg="#f0f2f5")
btn_frame.pack(pady=10)

def styled_btn(master, text, command, color):
    return tk.Button(master, text=text, command=command,
                     font=('Arial', 10, 'bold'), bg=color, fg='white',
                     activebackground='#333333', relief='flat', padx=15, pady=8)

styled_btn(btn_frame, "Add Expense", Add_items, "#28a745").grid(row=0, column=0, padx=10)
styled_btn(btn_frame, "Update Selected", Update_item, "#17a2b8").grid(row=0, column=1, padx=10)
styled_btn(btn_frame, "Delete Selected", Delete_item, "#dc3545").grid(row=0, column=2, padx=10)

# ---------- LAUNCH ----------
Refresh_items()
root.mainloop()
