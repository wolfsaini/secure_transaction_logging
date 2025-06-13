import hashlib
import psycopg2
from datetime import datetime

def connect_db():
    conn = psycopg2.connect(
        dbname="secure_transaction",
        user="postgres",
        password="saini121",
        host="localhost",
        port="5432"
    )
    print("Database connected.")
    return conn

def hash_transaction(transaction):
    record = (
        f"{transaction['transaction_id']}"
        f"{transaction['user_ID']}"
        f"{transaction['amount']}"
        f"{transaction['timestamp']}"
        f"{transaction['merchant_id']}"
        f"{transaction['product_id']}"
        f"{transaction['product_name']}"
        f"{transaction['product_price']}"
        f"{transaction['product_category']}"
    )
    return hashlib.sha256(record.encode('utf-8')).hexdigest()

def log_transaction(conn, transaction):
    # Input validation
    if not transaction['transaction_id'] or not transaction['user_ID']:
        print("Missing required fields.")
        return
    if transaction['amount'] <= 0 or transaction['product_price'] <= 0:
        print("Amount and product price must be greater than 0.")
        return

    hash_value = hash_transaction(transaction)

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO transactions (
                transaction_id, user_ID, amount, timestamp, merchant_id, 
                product_id, product_name, product_price, product_category, hash_value
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            transaction['transaction_id'],
            transaction['user_ID'],
            transaction['amount'],
            transaction['timestamp'],
            transaction['merchant_id'],
            transaction['product_id'],
            transaction['product_name'],
            transaction['product_price'],
            transaction['product_category'],
            hash_value
        ))
    conn.commit()
    print(f"Transaction {transaction['transaction_id']} logged successfully.")


def verify_transaction(conn, transaction_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM transactions WHERE transaction_id = %s", (transaction_id,))
        row = cur.fetchone()
        if not row:
            print("Transaction not found.")
            return False
        
        transaction = {
            "transaction_id": row[0],
            "user_ID": row[1],
            "amount": float(row[2]),
            "timestamp": row[3].strftime("%Y-%m-%d %H:%M:%S"),
            "merchant_id": row[4],
            "product_id": row[5],
            "product_name": row[6],
            "product_price": float(row[7]),
            "product_category": row[8]
        }

        stored_hash = row[9]
        computed_hash = hash_transaction(transaction)

        if stored_hash == computed_hash:
            print("Hash verified: Transaction is valid.")
            return True
        else:
            print("Hash mismatch: Data may be tampered.")
            return False
