import sqlite3
from datetime import datetime

def create_database():
    
    conn = sqlite3.connect("incidents.db")  # Connect to database file (creates it if it doesn't exist)
    c = conn.cursor()   # Cursor is used to execute SQL commands

    # Drop BOTH tables to avoid duplicates on rerun
    c.execute("DROP TABLE IF EXISTS incidents")
    c.execute("DROP TABLE IF EXISTS alerts")
    
    # Create incidents table
    c.execute("""
    CREATE TABLE incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id TEXT UNIQUE,
        incident_name TEXT,
        severity TEXT,
        status TEXT,
        classification TEXT,
        determination TEXT,
        created_time TEXT,
        last_update_time TEXT,
        assigned_to TEXT,
        threat_family TEXT,
        summary TEXT,
        machines INTEGER,
        users INTEGER,
        mailboxes INTEGER
    )
    """)
   
    # Create alerts table
    c.execute("""
    CREATE TABLE alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT,
        incident_id TEXT,
        title TEXT,
        category TEXT,
        severity TEXT,
        detection_source TEXT,
        machine_id TEXT,
        computer_dns_name TEXT,
        first_seen TEXT,
        last_seen TEXT,
        inserted_at TEXT,
        FOREIGN KEY (incident_id) REFERENCES incidents (incident_id)
    )
    """)
    
    conn.commit()  # Save changes
    conn.close()   # Close connection

def store_incidents(data):
    conn = sqlite3.connect("incidents.db")
    c = conn.cursor()

    total_incidents = 0     # Counter for inserted alerts
    total_alerts = 0        # Counter for inserted alerts

    try:
        # Loop through incidents
        for incident in data.get("value", []):
            
            # Insert incidents
            c.execute("""
            INSERT INTO incidents (
                incident_id,
                incident_name,
                severity,
                status,
                classification,
                determination,
                created_time,
                last_update_time,
                assigned_to,
                threat_family,
                summary,
                machines,
                users,
                mailboxes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                incident.get("incidentId"),
                incident.get("incidentName"),
                incident.get("severity"),
                incident.get("status"),
                incident.get("classification"),
                incident.get("determination"),
                incident.get("createdTime"),
                incident.get("lastUpdateTime"),
                incident.get("assignedTo"),
                incident.get("threatFamily"),
                incident.get("summary"),
                incident.get("impactedEntities", {}).get("machines"),
                incident.get("impactedEntities", {}).get("users"),
                incident.get("impactedEntities", {}).get("mailboxes")
            ))
            total_incidents += 1 # Count inserted incidents

            for alert in incident.get("alerts", []):

                c.execute("""
                INSERT INTO alerts (
                    alert_id,
                    incident_id,
                    title,
                    category,
                    severity,
                    detection_source,
                    machine_id,
                    computer_dns_name,
                    first_seen,
                    last_seen,
                    inserted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert.get("alertId"),
                    incident.get("incidentId"),
                    alert.get("title"),
                    alert.get("category"),
                    alert.get("severity"),
                    alert.get("detectionSource"),
                    alert.get("machineId"),
                    alert.get("computerDnsName"),
                    alert.get("firstActivity") or alert.get("firstSeen"),
                    alert.get("lastSeen"),
                    datetime.now().isoformat()
                ))
                total_alerts += 1 # Count inserted alerts

        conn.commit()

    except sqlite3.Error as e:
        print("Database error:", e)
        conn.rollback()  # Undo changes if something fails

    finally:
        conn.close()

    return total_incidents, total_alerts  # Return number of inserted incidents and alerts