# This code creates a simple GUI application using Tkinter to verify the integrity of transactions
import tkinter as tk
from tkinter import messagebox
from transaction_logger import connect_db, verify_transaction

def verify_hash():
    txn_id = txn_id_entry.get().strip()
    if not txn_id:
        messagebox.showerror("Input Error", "Transaction ID cannot be empty.")
        return

    conn = connect_db()
    result = verify_transaction(conn, txn_id)
    conn.close()

    if result:
        messagebox.showinfo("Verification Result", f" Transaction {txn_id} is VALID.\nHash matches.")
    else:
        messagebox.showwarning("Verification Result", f" Transaction {txn_id} is INVALID or TAMPERED.")

# main window
root = tk.Tk()
root.title("Transaction Hash Verifier")
root.geometry("400x200")

# Title
tk.Label(root, text="Verify Transaction Integrity", font=("Arial", 14, "bold")).pack(pady=10)

# Input field
tk.Label(root, text="Enter Transaction ID:").pack()
txn_id_entry = tk.Entry(root, width=30)
txn_id_entry.pack(pady=5)

# Verify button
verify_btn = tk.Button(root, text="Verify", command=verify_hash, bg="blue", fg="white", width=20)
verify_btn.pack(pady=15)

# Run the app
root.mainloop()
