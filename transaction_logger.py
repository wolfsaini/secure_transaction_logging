def log_transaction(conn, transaction):
    
    if not transaction['transaction_id'] or not transaction['user_ID']:
        print("Missing required fields.")
        return
    if transaction['amount'] <= 0 or transaction['product_price'] <= 0:
        print("Amount and product price must be greater than 0.")
        return

   
    hash_value = hash_transaction(transaction)
    
    def hash_transaction(transaction):
        import hashlib
        transaction_string = f"{transaction['transaction_id']}{transaction['user_ID']}{transaction['amount']}{transaction['timestamp']}{transaction['merchant_id']}{transaction['product_id']}{transaction['product_name']}{transaction['product_price']}{transaction['product_category']}"
        return hashlib.sha256(transaction_string.encode('utf-8')).hexdigest()

    with conn.cursor() as cur:
        cur.execute((
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
    print("Transaction logged successfully.")
