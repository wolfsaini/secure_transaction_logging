# 💼 Secure Transaction Logging & Anomaly Detection

A robust GUI-based Python application for securely logging transactions, detecting financial anomalies, and visualizing suspicious activity using both rule-based and unsupervised machine learning approaches.

---

## 🧾 Features

- ✅ Log transactions into a PostgreSQL database
- 🔐 Generate transaction hashes for verification
- 📊 Detect anomalies using:
  - Rule-based filters: `amount > ₹10,000`, `>5 txns/hour`
  - KMeans clustering (unsupervised ML)
- 📈 Visualize cluster distributions via Seaborn charts
- 🧠 Highlight and store anomalies in `anomalies.db` (SQLite)
- 📋 Export data and reports (`.csv`, `.txt`)
- 🔍 Filter dataset by user ID
- 🌈 GUI with color-highlighted anomaly records

---

## 📌 Technologies Used

| Tool               | Purpose                                  |
|--------------------|------------------------------------------|
| Python (Tkinter)   | GUI                                      |
| PostgreSQL         | Secure transaction storage               |
| SQLite             | Lightweight anomaly log                  |
| Pandas, Matplotlib | Data processing and visualization        |
| Seaborn            | Cluster plots                            |
| scikit-learn       | KMeans clustering for anomaly detection  |

---

## ⚙️ Installation

```bash
pip install pandas numpy seaborn scikit-learn psycopg2 matplotlib
```

---

## 🛠️ Configuration

Ensure PostgreSQL is running and contains a database:
```
Database: secure_transaction
Table: transactions
```

The table should have the following columns:

- `transaction_id`, `user_ID`, `amount`, `timestamp`, `merchant_id`
- `product_id`, `product_name`, `product_price`, `product_category`
- `hash` (SHA256 hash of all fields for tamper detection)

---

## 🚀 Running the App

```bash
python unified_GUI.py
```

---

## 📤 Output Files

- `anomalies.db`: SQLite DB with anomaly logs
- `anomaly_report_YYYYMMDD.txt`: Human-readable text report
- `dataset_export_YYYYMMDD.csv`: Exported transaction data
- Cluster chart: displayed in GUI (not saved by default)

---

## 🔍 Example Anomalies

| Type               | Description                     |
|--------------------|----------------------------------|
| Amount Anomaly     | `amount > ₹10,000`              |
| Frequency Anomaly  | `> 5 transactions/hour`         |
| Cluster Anomaly    | Top 5% outliers by distance from cluster center

---

## 📈 Visual Output

- Seaborn chart of clusters by `amount` vs. `product_price`
- Red `X` markers indicate cluster centers
- Each point colored by cluster membership

---

## 📚 Future Scope

- [ ] Export cluster chart to PNG
- [ ] Filter by date/amount range
- [ ] Email alerts for anomalies
- [ ] User-based authentication and roles

---

## 👨‍💻 Author

**Abhay Saini**  
Cybersecurity Internship Project  


