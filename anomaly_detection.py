import sqlite3

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
    print("Anomaly database setup complete.")

import pandas as pd
import psycopg2
from transaction_logger import connect_db
from datetime import datetime
from anomaly_detection import setup_anomaly_db
import sqlite3

def detect_anomalies():
    conn = connect_db()
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()

    flagged = []

    # Rule 1: Amount > 10,000
    high_amounts = df[df['amount'] > 10000]
    for _, row in high_amounts.iterrows():
        flagged.append((row['transaction_id'], row['user_ID'], row['amount'], row['timestamp'], "Amount > $10,000"))

    # Rule 2: More than 5 transactions/hour per user
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.floor('H')
    grouped = df.groupby(['user_ID', 'hour']).size().reset_index(name='txn_count')
    frequent_users = grouped[grouped['txn_count'] > 5]

    for _, row in frequent_users.iterrows():
        subset = df[(df['user_ID'] == row['user_ID']) & (df['hour'] == row['hour'])]
        for _, txn in subset.iterrows():
            flagged.append((txn['transaction_id'], txn['user_ID'], txn['amount'], txn['timestamp'], "More than 5 txns/hr"))

    # Store in SQLite
    setup_anomaly_db()
    sqlite_conn = sqlite3.connect("anomalies.db")
    cur = sqlite_conn.cursor()
    for anomaly in flagged:
        try:
            cur.execute("INSERT INTO anomalies VALUES (?, ?, ?, ?, ?)", anomaly)
        except sqlite3.IntegrityError:
            continue  # Skip duplicates
    sqlite_conn.commit()
    sqlite_conn.close()

    print(f"{len(flagged)} anomalies detected and stored.")

def generate_anomaly_report():
    conn = sqlite3.connect("anomalies.db")
    df = pd.read_sql("SELECT * FROM anomalies", conn)
    conn.close()

    if df.empty:
        print("No anomalies to report.")
        return

    filename = f"anomaly_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write("Anomaly Report\n")
        f.write("=" * 50 + "\n")
        for _, row in df.iterrows():
            f.write(f"Txn ID: {row['transaction_id']} | User: {row['user_ID']} | Amount: {row['amount']} | Time: {row['timestamp']} | Reason: {row['reason']}\n")
    print(f"Report saved as {filename}")

