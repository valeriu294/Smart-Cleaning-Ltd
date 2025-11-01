import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import base64
from xml.etree import ElementTree as ET
import re


# --- Database setup ---
DB_PATH = "smartCleaningLTD.db"


#--- Database functions ---
def connect_db():
    return sqlite3.connect(DB_PATH)

def insert_customer():
    fname = entry_fname.get().strip()
    lname = entry_lname.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    if not fname or not lname:
        messagebox.showerror("Error", "First and Last name required")
        return
    try:
        with connect_db() as conn:
            conn.execute("INSERT INTO customer(first_name, last_name, phone, email) VALUES (?,?,?,?)",
                         (fname, lname, phone, email))
        messagebox.showinfo("Success", "Customer added successfully.")
        load_customers()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

def load_customers():
    for i in tree.get_children():
        tree.delete(i)
    with connect_db() as conn:
        for row in conn.execute("SELECT customer_id, first_name, last_name, phone, email FROM customer"):
            tree.insert("", tk.END, values=row)


#--- Database connection check ---
def check_db_connection():
    try:
        with connect_db() as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
        return True, "Database connection successful ✔"
    except Exception as e:
        return False, f"Database error: {e}"
    
# Dark mode toggle
    
def toggle_theme():
    current = root.cget("bg")
    new = "#333333" if current == "SystemButtonFace" else "SystemButtonFace"
    root.config(bg=new)

    

    
    
 # Quit application   
def quit_app():
    confirm = messagebox.askyesno("Exit", "Are you sure you want to quit?")
    if confirm:
        root.destroy()

    
 # Delete customer   
def delete_customer():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select", "Please select a customer to delete.")
        return
    cid = tree.item(selected)["values"][0]
    name = f"{tree.item(selected)['values'][1]} {tree.item(selected)['values'][2]}"
    
    confirm = messagebox.askyesno("Confirm Delete", f"Delete customer {name} (ID {cid})?")
    if not confirm:
        return
    try:
        with connect_db() as conn:
            conn.execute("DELETE FROM customer WHERE customer_id = ?", (cid,))
        messagebox.showinfo("Deleted", f"Customer {name} deleted successfully.")
        load_customers()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))


# --- GUI setup ---
root = tk.Tk()
root.title("SmartClean Customer Manager")
root.geometry("700x500")

# Status bar
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, anchor="w", padx=8)
status_label.pack(fill="x", side="bottom")

# Input frame
frm = tk.Frame(root, pady=10)
frm.pack()

# Input fields
tk.Label(frm, text="First Name").grid(row=0, column=0)
tk.Label(frm, text="Last Name").grid(row=0, column=2)
tk.Label(frm, text="Phone").grid(row=1, column=0)
tk.Label(frm, text="Email").grid(row=1, column=2)

entry_fname = tk.Entry(frm, width=20)
entry_lname = tk.Entry(frm, width=20)
entry_phone = tk.Entry(frm, width=20)
entry_email = tk.Entry(frm, width=20)

entry_fname.grid(row=0, column=1)
entry_lname.grid(row=0, column=3)
entry_phone.grid(row=1, column=1)
entry_email.grid(row=1, column=3)

tk.Button(frm, text="Add", command=insert_customer, bg="#4CAF50", fg="white").grid(row=2, column=0, pady=5)
tk.Button(frm, text="Delete", command=delete_customer, bg="#f44336", fg="white").grid(row=2, column=1, pady=5)
tk.Button(frm, text="Refresh", command=load_customers).grid(row=2, column=2, pady=5)
tk.Button(frm, text="Toggle Theme", command=toggle_theme).grid(row=2, column=3, pady=5)
tk.Button(frm, text="Quit", command=quit_app, bg="#6c757d", fg="white").grid(row=2, column=7, pady=5, padx=5)


tree = ttk.Treeview(root, columns=("ID", "First", "Last", "Phone", "Email"), show="headings")
for col in ("ID", "First", "Last", "Phone", "Email"):
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True, pady=10)


#--- Initial DB connection check ---
ok, msg = check_db_connection()
status_var.set(msg)
if ok:
    status_label.config(bg="#d4edda", fg="#155724")   # green
else:
    status_label.config(bg="#f8d7da", fg="#721c24")   # red
    
#--- Handle window close ---   
def on_close():
    if messagebox.askokcancel("Exit", "Do you really want to quit the application?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)







load_customers()
root.mainloop()
