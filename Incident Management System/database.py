import sqlite3                  # Built-in Python database module (SQLite)
from datetime import datetime  # Used to generate timestamps

def create_database():
    # Connect to database file (creates it if it doesn't exist)
    conn = sqlite3.connect("incidents.db")
    c = conn.cursor()  # Cursor is used to execute SQL commands

    # Drop table every run → prevents duplicate data
    # (Useful for assignments, not typical in production systems)
    c.execute("DROP TABLE IF EXISTS alerts")

    # Create alerts table based on assignment requirements
    c.execute("""
    CREATE TABLE alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique internal ID
        alert_id TEXT,                         -- Alert identifier from API
        incident_id TEXT,                      -- Related incident ID
        category TEXT,                         -- Type of threat (Malware, C2, etc.)
        machine_id TEXT,                       -- Machine affected
        first_seen TEXT,                       -- First detection timestamp
        detection_source TEXT,                 -- Microsoft product that detected it
        inserted_at TEXT                       -- When we stored it (required by assignment)
    )
    """)

    conn.commit()  # Save changes
    conn.close()   # Close connection (very important)

def store_incidents(data):
    # Open database connection
    conn = sqlite3.connect("incidents.db")
    c = conn.cursor()

    total_alerts = 0  # Counter for inserted alerts

    try:
        # Loop through incidents
        for incident in data.get("value", []):

            # Extract incident ID once (used for all alerts inside)
            incident_id = incident.get("incidentId")

            # Loop through alerts inside each incident
            for alert in incident.get("alerts", []):

                # Insert alert into database using parameterized query
                # (prevents SQL injection and formatting errors)
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
                    alert.get("alertId"),                             # Alert ID
                    incident_id,                                      # Parent incident ID
                    alert.get("category"),                            # Threat category
                    alert.get("machineId"),                           # Machine affected
                    alert.get("firstSeen") or alert.get("firstActivity"),  # Handle API inconsistency
                    alert.get("detectionSource"),                     # Detection system
                    datetime.now().isoformat()                        # Current timestamp
                ))

                total_alerts += 1  # Count inserted alert

        conn.commit()  # Save all inserts

    except sqlite3.Error as e:
        print("Database error:", e)
        conn.rollback()  # Undo changes if something fails

    finally:
        conn.close()  # Always close connection

    return total_alerts  # Return number of inserted alerts