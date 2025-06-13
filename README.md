📘 README: Secure Transaction Logging & Anomaly Detection
🔐 Project Title
Secure Transaction Logging and Anomaly Detection

👨‍💻 Developer
Abhay Saini

📌 Project Description
This application provides a secure way to log transaction data into a PostgreSQL database and detect anomalies using both:

✅ Rule-based methods (e.g., high-value, high-frequency)

✅ Unsupervised machine learning (KMeans clustering)

The GUI interface, built with Tkinter, allows users to:

1.Log transactions

2.Verify integrity

3.View, search, and export datasets

4.Visualize cluster-based anomaly detection

📂 Features

Feature	Description

✅ Log Transactions	Record new transactions into PostgreSQL

🔍 Detect Anomalies	Flags: amount > ₹10,000, >5 txns/hour, or cluster outliers

📄 Anomaly Report	Generates a .txt report with all flagged anomalies

📊 Cluster Visualization	KMeans scatter plot with seaborn

🗃️ View Dataset	View all transactions with search and export options

🌈 Highlighting	Anomalies appear in red in the dataset viewer

📤 Export to CSV	One-click export of transaction logs

🎛️ Filter by User	Filter transactions by User ID

🏗️ Technologies Used

🐍 Python 3.10+

🎨 Tkinter for GUI

🐘 PostgreSQL (via psycopg2)

📊 Pandas & Seaborn for plotting

🤖 Scikit-learn for anomaly detection (KMeans)

📁 SQLite for storing flagged anomalies

⚙️ How to Run

1.Install dependencies
  pip install pandas scikit-learn matplotlib seaborn psycopg2
  
2.Ensure PostgreSQL is running

  Database: secure_transaction

  Table: transactions

3.Launch the GUI
  python unified_GUI.py
  
💡 Anomaly Detection Rules

Type	Description
Amount Anomaly	amount > ₹10,000

Frequency Anomaly	> 5 txns/hour for the same user

Cluster Anomaly	Far from cluster center (top 5% distance)

🧪 Sample Data You Can Use

json
Copy
Edit
{
  "transaction_id": "TXN1001",
  "user_ID": "USR999",
  "amount": 12500,
  "merchant_id": "MRC100",
  "product_id": "PRD200",
  "product_name": "Smartphone",
  "product_price": 12500,
  "product_category": "Electronics"
}

📦 Outputs

anomalies.db: Local SQLite DB with flagged anomalies

anomaly_report_YYYYMMDD.txt: Human-readable report

dataset_export_YYYYMMDD.csv: Exported data from the GUI

