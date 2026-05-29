import sqlite3

DB_PATH = "donations.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            location TEXT,
            blood_type TEXT,
            pints REAL DEFAULT 1.0
        )
    """)
    conn.commit()
    conn.close()

def get_history():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        "SELECT id, date, location, blood_type, pints FROM donations ORDER BY date DESC"
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_latest_donation_date() -> str | None:
    conn = get_connection()
    cursor = conn.execute("SELECT date FROM donations ORDER BY date DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_total_pints() -> float:
    conn = get_connection()
    cursor = conn.execute("SELECT SUM(pints) FROM donations")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row[0] is not None else 0.0

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")