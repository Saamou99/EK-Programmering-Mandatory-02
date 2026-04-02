import sqlite3

def create_database():
    conn = sqlite3.connect("incidents.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        incidentId      TEXT,
        incidentName    TEXT,
        severity        TEXT,
        status          TEXT,
        lastUpdateTime  TEXT,
        summary         TEXT,
        machines        INTEGER
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
                incidentId, incidentName, severity,
                status, lastUpdateTime, summary, machines
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.get("incidentId"),
                alert.get("incidentName"),
                alert.get("severity"),
                alert.get("status"),
                alert.get("lastUpdateTime"),
                alert.get("summary"),
                alert.get("machines")
            ))

        conn.commit()

    except sqlite3.Error as e:
        print("Database error:", e)
        conn.rollback()  # VERY IMPORTANT (your assignment requires this)

    finally:
        conn.close()