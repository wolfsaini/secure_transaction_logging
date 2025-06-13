import tkinter as tk
from tkinter import messagebox
from transaction_logger import connect_db, log_transaction
from datetime import datetime
def submit_transaction():
    transaction = {
        "transaction_id": txn_id_entry.get(),
        "user_ID": user_id_entry.get(),
        "amount": float(amount_entry.get()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "merchant_id": merchant_id_entry.get(),
        "product_id": product_id_entry.get(),
        "product_name": product_name_entry.get(),
        "product_price": float(product_price_entry.get()),
        "product_category": product_category_entry.get()
    }

    conn = connect_db()
    log_transaction(conn, transaction)
    conn.close()

    messagebox.showinfo("Success", "Transaction logged successfully.")
    clear_form()


def clear_form():
    global txn_id_entry, user_id_entry, amount_entry, merchant_id_entry, product_id_entry, product_name_entry, product_price_entry, product_category_entry
    for entry in [txn_id_entry, user_id_entry, amount_entry, merchant_id_entry, 
                  product_id_entry, product_name_entry, product_price_entry, product_category_entry]:
        entry.delete(0, tk.END)


root = tk.Tk()
root.title("Secure Transaction Logger")
root.geometry("400x500")


fields = [
    ("Transaction ID", "txn_id_entry"),
    ("User ID", "user_id_entry"),
    ("Amount", "amount_entry"),
    ("Merchant ID", "merchant_id_entry"),
    ("Product ID", "product_id_entry"),
    ("Product Name", "product_name_entry"),
    ("Product Price", "product_price_entry"),
    ("Product Category", "product_category_entry")
]

for idx, (label_text, var_name) in enumerate(fields):
    tk.Label(root, text=label_text).grid(row=idx, column=0, padx=10, pady=5, sticky='w')
    entry = tk.Entry(root, width=30)
    entry.grid(row=idx, column=1)
    globals()[var_name] = entry
submit_btn = tk.Button(root, text="Log Transaction", command=lambda: submit_transaction(), bg="green", fg="white")
submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)

root.mainloop()
