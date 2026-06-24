import sqlite3

DB_NAME = "honeypot.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        ip_address TEXT NOT NULL,
        username TEXT,
        password TEXT,
        user_agent TEXT,
        country TEXT,
        city TEXT,
        threat_score INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def save_attempt(ip, username, password, user_agent, country="Unknown", city="Unknown", threat_score=0):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO attempts (ip_address, username, password, user_agent, country, city, threat_score)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ip, username, password, user_agent, country, city, threat_score))

    conn.commit()
    conn.close()


def get_all_logs(limit=500):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM attempts
    ORDER BY timestamp DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_recent_attempts(ip, minutes=10):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM attempts
    WHERE ip_address = ?
    AND timestamp >= datetime('now', ?)
    ORDER BY timestamp DESC
    """, (ip, f'-{minutes} minutes'))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_top_usernames(limit=10):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, COUNT(*) as count
    FROM attempts
    GROUP BY username
    ORDER BY count DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_attempts_by_hour():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
    FROM attempts
    GROUP BY hour
    ORDER BY hour
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_high_threat_ips(min_score=50):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT ip_address, username, threat_score, timestamp
    FROM attempts
    WHERE threat_score >= ?
    ORDER BY threat_score DESC
    """, (min_score,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
