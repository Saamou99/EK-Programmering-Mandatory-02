import sqlite3

def create_database():
    conn = sqlite3.connect("incidents.db")
    c = conn.cursor()

    c.execute("""
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
    conn.close()

def store_incidents(data):
    conn = sqlite3.connect("incidents.db")
    c = conn.cursor()

    try:
        for alert in data.get("value", []):
            c.execute("""
            INSERT INTO alerts (
                alertID, incidentId, category,
                machineID, firstSeen, timestamp, detectionSource
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.get("alertID"),
                alert.get("incidentId"),
                alert.get("category"),
                alert.get("machineID"),
                alert.get("firstSeen"),
                alert.get("timestamp"),
                alert.get("detectionSource")
            ))

        conn.commit()

    except sqlite3.Error as e:
        print("Database error:", e)
        conn.rollback()  # VERY IMPORTANT (your assignment requires this)

    finally:
        conn.close()