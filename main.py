from transaction_logger import connect_db, log_transaction
from datetime import datetime

transaction = {
    "transaction_id": "TXN9066",
    "user_ID": "USR8906",
    "amount": 25798.00,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "merchant_id": "MRC9845",
    "product_id": "PRD65422",
    "product_name": "Smartphone",
    "product_price": 25798.00,
    "product_category": "Electronics"
}

if __name__ == "__main__":
    conn = connect_db()
    log_transaction(conn, transaction)
    conn.close()
