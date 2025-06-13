import tkinter as tk
from tkinter import ttk, messagebox
from transaction_logger import connect_db, log_transaction, verify_transaction
from datetime import datetime
import csv
import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

# ------------------------------
# Anomaly Detection Functions
# ------------------------------
def setup_anomaly_db():
    conn = sqlite3.connect("anomalies.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS anomalies (
            transaction_id TEXT PRIMARY KEY,
            user_ID TEXT,
            amount REAL,
            timestamp TEXT,
            reason TEXT
        )
    """)
    conn.commit()
    conn.close()

def cluster_based_anomalies(df, anomalies):
    if 'amount' not in df.columns or 'product_price' not in df.columns:
        return

    # Keep meta data
    meta_cols = df[['transaction_id', 'user_id', 'timestamp']].reset_index(drop=True)
    df_numeric = df[['amount', 'product_price']].reset_index(drop=True)

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_numeric)

    # Fit KMeans
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    cluster_labels = kmeans.fit_predict(X_scaled)
    distances = np.linalg.norm(X_scaled - kmeans.cluster_centers_[cluster_labels], axis=1)

    df_clusters = pd.concat([meta_cols, df_numeric], axis=1)
    df_clusters['cluster'] = cluster_labels
    df_clusters['distance'] = distances

    threshold = np.percentile(df_clusters['distance'], 95)
    anomaly_df = df_clusters[df_clusters['distance'] > threshold]
    for _, row in anomaly_df.iterrows():
        anomalies.append((row['transaction_id'], row['user_id'], row['amount'], str(row['timestamp']), "Cluster anomaly (KMeans)"))

def detect_anomalies():
    setup_anomaly_db()
    pg_conn = connect_db()
    df = pd.read_sql("SELECT * FROM transactions", pg_conn)
    df.columns = [col.lower() for col in df.columns]
    pg_conn.close()

    if df.empty:
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    anomalies = []

    high_amount = df[df['amount'] > 10000]
    for _, row in high_amount.iterrows():
        anomalies.append((row['transaction_id'], row['user_id'], row['amount'], str(row['timestamp']), "Amount > $10,000"))

    df['hour'] = df['timestamp'].dt.floor('H')
    counts = df.groupby(['user_id', 'hour']).size().reset_index(name='txn_count')
    flagged_groups = counts[counts['txn_count'] > 5]

    for _, group in flagged_groups.iterrows():
        user_txns = df[(df['user_id'] == group['user_id']) & (df['hour'] == group['hour'])]
        for _, row in user_txns.iterrows():
            anomalies.append((row['transaction_id'], row['user_id'], row['amount'], str(row['timestamp']), "More than 5 txns/hr"))

    cluster_based_anomalies(df, anomalies)

    conn = sqlite3.connect("anomalies.db")
    cur = conn.cursor()
    for entry in anomalies:
        try:
            cur.execute("INSERT INTO anomalies VALUES (?, ?, ?, ?, ?)", entry)
        except sqlite3.IntegrityError:
            continue
    conn.commit()
    conn.close()

def generate_anomaly_report():
    conn = sqlite3.connect("anomalies.db")
    df = pd.read_sql("SELECT * FROM anomalies", conn)
    conn.close()
    if df.empty:
        print("No anomalies found.")
        return
    filename = f"anomaly_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write("Anomaly Report\n")
        f.write("=" * 50 + "\n")
        for _, row in df.iterrows():
            f.write(f"Txn: {row['transaction_id']} | User: {row['user_ID']} | Amount: {row['amount']} | Time: {row['timestamp']} | Reason: {row['reason']}\n")
    print(f"✅ Anomaly report saved as: {filename}")

# ------------------------------
# GUI + Submission Logic
# ------------------------------
root = tk.Tk()
root.title("Secure Transaction Logger & Anomaly Detector")
root.geometry("800x850")

# --- Transaction Entry Fields ---
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

fields = ["Transaction ID", "User ID", "Amount", "Merchant ID", "Product ID", "Product Name", "Product Price", "Product Category"]
entries = {}

for i, field in enumerate(fields):
    tk.Label(form_frame, text=field).grid(row=i, column=0, sticky='w', padx=5, pady=2)
    entry = tk.Entry(form_frame, width=40)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entries[field] = entry

# --- Functions using your existing backend ---
def submit_transaction():
    try:
        data = {
            "transaction_id": entries["Transaction ID"].get(),
            "user_ID": entries["User ID"].get(),
            "amount": float(entries["Amount"].get()),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "merchant_id": entries["Merchant ID"].get(),
            "product_id": entries["Product ID"].get(),
            "product_name": entries["Product Name"].get(),
            "product_price": float(entries["Product Price"].get()),
            "product_category": entries["Product Category"].get()
        }
        conn = connect_db()
        log_transaction(conn, data)
        conn.close()
        detect_anomalies()
        messagebox.showinfo("Success", "Transaction logged and anomaly check complete.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_anomalies():
    detect_anomalies()
    conn = sqlite3.connect("anomalies.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM anomalies ORDER BY timestamp DESC")
    rows = cur.fetchall()
    conn.close()

    result_window = tk.Toplevel(root)
    result_window.title("Anomalies Found")
    result_window.geometry("700x400")

    listbox = tk.Listbox(result_window, width=100)
    listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for row in rows:
        display = f"Txn: {row[0]} | User: {row[1]} | Amount: {row[2]} | Time: {row[3]} | Reason: {row[4]}"
        listbox.insert(tk.END, display)

def export_report():
    generate_anomaly_report()
    messagebox.showinfo("Report", "Anomaly report generated and saved.")

# --- Cluster Visualization ---
def show_cluster_chart():
    pg_conn = connect_db()
    df = pd.read_sql("SELECT * FROM transactions", pg_conn)
    df.columns = [col.lower() for col in df.columns]
    pg_conn.close()

    if df.empty or 'amount' not in df.columns or 'product_price' not in df.columns:
        messagebox.showerror("Error", "Not enough data for clustering.")
        return

    import matplotlib.pyplot as plt
    import seaborn as sns

    df_numeric = df[['amount', 'product_price']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_numeric)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    clusters = kmeans.fit_predict(X_scaled)
    df['cluster'] = clusters

    plt.figure(figsize=(10, 7))
    sns.set(style="whitegrid")
    palette = sns.color_palette("viridis", as_cmap=False)

    sns.scatterplot(
        x='amount',
        y='product_price',
        hue='cluster',
        palette=palette,
        data=df,
        s=100,
        edgecolor='black',
        alpha=0.8
    )

    centers = scaler.inverse_transform(kmeans.cluster_centers_)
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=300, alpha=0.9, marker='X', label='Centers')

    plt.title("KMeans Cluster Distribution", fontsize=14)
    plt.xlabel("Transaction Amount", fontsize=12)
    plt.ylabel("Product Price", fontsize=12)
    plt.legend(title="Cluster")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --- View Dataset ---
def show_dataset():
    pg_conn = connect_db()
    df = pd.read_sql("SELECT * FROM transactions ORDER BY timestamp DESC", pg_conn)
    df.columns = [col.lower() for col in df.columns]
    pg_conn.close()

    anomalies_df = pd.read_sql("SELECT transaction_id FROM anomalies", sqlite3.connect("anomalies.db"))
    anomaly_txns = set(anomalies_df['transaction_id'])

    view_window = tk.Toplevel(root)
    view_window.title("Transaction Dataset")
    view_window.geometry("1000x500")

    frame = tk.Frame(view_window)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor='center')

    style = ttk.Style()
    style.map("Treeview", background=[('selected', '#ececec')])

    for _, row in df.iterrows():
        values = list(row)
        tags = ('anomaly',) if row['transaction_id'] in anomaly_txns else ()
        tree.insert('', tk.END, values=values, tags=tags)

    tree.tag_configure('anomaly', background='salmon')

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def export_to_csv():
        filename = f"dataset_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        messagebox.showinfo("Export", f"Dataset exported to {filename}")

    filter_frame = tk.Frame(view_window)
    filter_frame.pack(pady=10)

    tk.Button(filter_frame, text="Export to CSV", command=export_to_csv, bg="teal", fg="white").pack(side=tk.LEFT, padx=10)

    def apply_user_filter():
        query = user_filter.get().strip()
        for i in tree.get_children():
            tree.delete(i)
        filtered = df[df['user_id'].str.contains(query, case=False, na=False)]
        for _, row in filtered.iterrows():
            tags = ('anomaly',) if row['transaction_id'] in anomaly_txns else ()
            tree.insert('', tk.END, values=list(row), tags=tags)

    tk.Label(filter_frame, text="Filter by User ID:").pack(side=tk.LEFT)
    user_filter = tk.Entry(filter_frame)
    user_filter.pack(side=tk.LEFT, padx=5)
    tk.Button(filter_frame, text="Apply Filter", command=apply_user_filter).pack(side=tk.LEFT)

# --- Buttons ---
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Log Transaction", command=submit_transaction, bg="green", fg="white").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Show Anomalies", command=show_anomalies, bg="blue", fg="white").grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Generate Report", command=export_report, bg="orange", fg="black").grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Show Cluster Chart", command=show_cluster_chart, bg="purple", fg="white").grid(row=0, column=3, padx=10)
tk.Button(btn_frame, text="View Dataset", command=show_dataset, bg="gray", fg="white").grid(row=0, column=4, padx=10)

# --- Mainloop to launch GUI ---
root.mainloop()
