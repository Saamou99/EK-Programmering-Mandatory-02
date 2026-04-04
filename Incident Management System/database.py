import sqlite3

def create_database():                                                  #Create database and table
    conn = sqlite3.connect("incidents.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id TEXT,
        incident_name TEXT,
        severity TEXT,
        status TEXT,
        last_update_time TEXT,
        summary TEXT,
        machines INTEGER
    )
    """)
    conn.commit()
    conn.close()

def store_incidents(data):                                              #Store incidents in database
    conn = sqlite3.connect("incidents.db")
    c = conn.cursor()

    try:
        for incident in data.get("value", []):                          #Loop through incidents

            c.execute("""
            INSERT INTO incidents (
                incident_id,
                incident_name,
                severity,
                status,
                last_update_time,
                summary,
                machines
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                incident.get("incidentId"),
                incident.get("incidentName"),
                incident.get("severity"),
                incident.get("status"),
                incident.get("lastUpdateTime"),
                incident.get("summary"),
                incident.get("impactedEntities", {}).get("machines")    #Nested JSON field
            ))

        conn.commit()
        print(f"Stored {len(data.get('value', []))} incidents")

    except sqlite3.Error as e:
        print("Database error:", e)
        conn.rollback()
    
    finally:
        conn.close()