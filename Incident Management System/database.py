import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect("incidents.db")
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS alerts")    #Drop table to avoid duplicates

    c.execute("""
    CREATE TABLE alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT,
        incident_id TEXT,
        category TEXT,
        machine_id TEXT,
        first_seen TEXT,
        detection_source TEXT,
        inserted_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def store_incidents(data):
    conn = sqlite3.connect("incidents.db")
    c = conn.cursor()

    total_alerts = 0

    try:
        for incident in data.get("value", []):

            incident_id = incident.get("incidentId")

            for alert in incident.get("alerts", []):

                c.execute("""
                INSERT INTO alerts (
                    alert_id,
                    incident_id,
                    category,
                    machine_id,
                    first_seen,
                    detection_source,
                    inserted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert.get("alertId"),
                    incident_id,
                    alert.get("category"),
                    alert.get("machineId"),
                    alert.get("firstSeen") or alert.get("firstActivity"),
                    alert.get("detectionSource"),
                    datetime.now().isoformat()
                ))

                total_alerts += 1

        conn.commit()

    except sqlite3.Error as e:
        print("Database error:", e)
        conn.rollback()

    finally:
        conn.close()

    return total_alerts