import sqlite3
from pathlib import Path

def get_conn(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = get_conn(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            service TEXT NOT NULL,
            severity TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            root_cause TEXT,
            resolution TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_incident(db_path, incident):
    conn = get_conn(db_path)
    cur = conn.execute("""
        INSERT INTO incidents(title, service, severity, symptoms, root_cause, resolution)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        incident["title"], incident["service"], incident["severity"],
        incident["symptoms"], incident.get("root_cause"), incident.get("resolution")
    ))
    conn.commit()
    incident_id = cur.lastrowid
    conn.close()
    return incident_id

def list_incidents(db_path):
    conn = get_conn(db_path)
    rows = conn.execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
