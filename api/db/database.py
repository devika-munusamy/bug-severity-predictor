import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "predictions.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Core predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            error_message      TEXT    NOT NULL,
            user_count         INTEGER NOT NULL,
            predicted_severity TEXT    NOT NULL,
            confidence         REAL    NOT NULL,
            impact_score       REAL    NOT NULL,
            error_category     TEXT    NOT NULL DEFAULT 'Unknown',
            timestamp          TEXT    NOT NULL
        )
    """)

    # Gracefully add `error_category` if the DB was created before this column existed
    try:
        cursor.execute("ALTER TABLE predictions ADD COLUMN error_category TEXT NOT NULL DEFAULT 'Unknown'")
    except sqlite3.OperationalError:
        pass  # column already present

    conn.commit()
    conn.close()


def save_prediction(
    error_message: str,
    user_count: int,
    severity: str,
    confidence: float,
    impact_score: float,
    error_category: str = "Unknown",
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions
          (error_message, user_count, predicted_severity, confidence,
           impact_score, error_category, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        error_message,
        user_count,
        severity,
        round(confidence, 4),
        round(impact_score, 4),
        error_category,
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    ))
    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, error_message, user_count, predicted_severity,
               confidence, impact_score, error_category, timestamp
        FROM predictions
        ORDER BY id DESC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows
