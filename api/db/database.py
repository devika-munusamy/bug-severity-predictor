import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "predictions.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            error_message     TEXT NOT NULL,
            user_count        INTEGER NOT NULL,
            predicted_severity TEXT NOT NULL,
            confidence        REAL NOT NULL,
            impact_score      REAL NOT NULL,
            timestamp         TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_prediction(error_message, user_count, severity, confidence, impact_score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions
          (error_message, user_count, predicted_severity, confidence, impact_score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        error_message,
        user_count,
        severity,
        round(confidence, 4),
        round(impact_score, 4),
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, error_message, user_count, predicted_severity,
               confidence, impact_score, timestamp
        FROM predictions
        ORDER BY id DESC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows
