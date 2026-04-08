import sqlite3
import pandas as pd

DB_NAME = "fraud.db"


# -----------------------------
# CREATE CONNECTION
# -----------------------------
def create_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# -----------------------------
# CREATE TABLE
# -----------------------------
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        transaction_hour INTEGER,
        foreign_transaction INTEGER,
        location_mismatch INTEGER,
        device_trust_score REAL,
        velocity_last_24h INTEGER,
        cardholder_age INTEGER,
        merchant_category TEXT,
        prediction INTEGER,
        probability REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# INSERT TRANSACTION
# -----------------------------
def insert_transaction(data: dict, pred: int, prob: float):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions (
        amount,
        transaction_hour,
        foreign_transaction,
        location_mismatch,
        device_trust_score,
        velocity_last_24h,
        cardholder_age,
        merchant_category,
        prediction,
        probability
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['amount'],
        data['transaction_hour'],
        data['foreign_transaction'],
        data['location_mismatch'],
        data['device_trust_score'],
        data['velocity_last_24h'],
        data['cardholder_age'],
        data['merchant_category'],
        int(pred),
        float(prob)
    ))

    conn.commit()
    conn.close()


# -----------------------------
# FETCH ALL TRANSACTIONS
# -----------------------------
def fetch_transactions():
    conn = create_connection()

    df = pd.read_sql_query(
        "SELECT * FROM transactions ORDER BY id DESC",
        conn
    )

    conn.close()
    return df


# -----------------------------
# FETCH ONLY FRAUDS
# -----------------------------
def fetch_fraud_transactions():
    conn = create_connection()

    df = pd.read_sql_query(
        "SELECT * FROM transactions WHERE prediction = 1 ORDER BY id DESC",
        conn
    )

    conn.close()
    return df


# -----------------------------
# DELETE ALL DATA (RESET)
# -----------------------------
def delete_all_transactions():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions")

    conn.commit()
    conn.close()


# -----------------------------
# GET BASIC STATS
# -----------------------------
def get_stats():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE prediction = 1")
    frauds = cursor.fetchone()[0]

    conn.close()

    fraud_rate = (frauds / total * 100) if total > 0 else 0

    return {
        "total_transactions": total,
        "fraud_transactions": frauds,
        "fraud_rate": round(fraud_rate, 2)
    }