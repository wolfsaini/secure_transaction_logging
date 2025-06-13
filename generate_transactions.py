from transaction_logger import connect_db, log_transaction
from datetime import datetime, timedelta
import random

def generate_transaction(i):
    return {
        "transaction_id": f"AUTO{i:04}",
        "user_ID": f"USR{random.randint(100, 999)}",
        "amount": round(random.uniform(50, 15000), 2),
        "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 60))).strftime("%Y-%m-%d %H:%M:%S"),
        "merchant_id": f"MRC{random.randint(1, 5)}",
        "product_id": f"PRD{random.randint(100, 999)}",
        "product_name": f"Product-{i}",
        "product_price": round(random.uniform(50, 15000), 2),
        "product_category": random.choice(["Electronics", "Books", "Clothing", "Groceries", "Utilities"])
    }

if __name__ == "__main__":
    conn = connect_db()
    for i in range(1, 101):
        txn = generate_transaction(i)
        log_transaction(conn, txn)
    conn.close()
    print("100+ transactions logged.")
