from transaction_logger import connect_db, log_transaction
from datetime import datetime

transaction = {
    "transaction_id": "TXN1001",
    "user_ID": "USR123",
    "amount": 2500.00,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "merchant_id": "MRC009",
    "product_id": "PRD001",
    "product_name": "Smartphone",
    "product_price": 2500.00,
    "product_category": "Electronics"
}

if __name__ == "__main__":
    conn = connect_db()
    log_transaction(conn, transaction)
    conn.close()
