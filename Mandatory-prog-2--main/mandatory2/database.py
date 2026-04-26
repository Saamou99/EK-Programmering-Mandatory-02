import sqlite3
from datetime import datetime

DB_FILE = "incidents.db"


def create_table():
    """Create the alerts table if it doesn't already exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                alertID         TEXT,
                incidentId      TEXT,
                category        TEXT,
                machineID       TEXT,
                firstSeen       TEXT,
                timestamp       TEXT,
                detectionSource TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()


def insert_alert(alert, incident_id, timestamp):
    """Insert a single alert into the database using parameterised queries."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO alerts (
                alertID, incidentId, category, machineID,
                firstSeen, timestamp, detectionSource
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            alert.get("alertId"),
            incident_id,
            alert.get("category"),
            alert.get("machineId"),
            alert.get("firstEventTime"),
            timestamp,
            alert.get("detectionSource")
        ))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error inserting alert: {e}")
    finally:
        conn.close()