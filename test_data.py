from transaction_logger import connect_db, log_transaction
from datetime import datetime, timedelta
import random

def generate_transaction(i, force_anomaly=False, freq_user=None):
    base_time = datetime.now().replace(minute=0, second=0, microsecond=0)

    # High amount anomaly every 5th transaction
    amount = random.uniform(100, 9000)
    if i % 5 == 0 or force_anomaly:
        amount = random.uniform(12000, 30000)

    user_id = f"USR{1000 + i}"
    if freq_user:
        user_id = freq_user

    return {
        "transaction_id": f"TXN{i:04}",
        "user_ID": user_id,
        "amount": round(amount, 2),
        "timestamp": (base_time + timedelta(minutes=random.randint(0, 50))).strftime("%Y-%m-%d %H:%M:%S"),
        "merchant_id": f"MRC{random.randint(100, 999)}",
        "product_id": f"PRD{random.randint(100, 999)}",
        "product_name": f"Product-{i}",
        "product_price": round(amount, 2),
        "product_category": random.choice(["Electronics", "Books", "Clothing", "Groceries"])
    }

def insert_transactions():
    conn = connect_db()

    # Insert 44 normal + high-amount mix
    for i in range(44):
        txn = generate_transaction(i)
        log_transaction(conn, txn)

    # Insert 6 transactions for one user in same hour (high-frequency anomaly)
    for j in range(44, 50):
        txn = generate_transaction(j, force_anomaly=False, freq_user="USRSPAM")
        log_transaction(conn, txn)

    conn.close()
    print("50 transactions inserted, including anomalies.")

if __name__ == "__main__":
    insert_transactions()
