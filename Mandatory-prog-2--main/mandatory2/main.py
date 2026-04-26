from api import get_token, fetch_incidents
from database import create_table, insert_alert, DB_FILE
from datetime import datetime
import json

def main():
    # Step 1: set up the database table
    print("Setting up database...")
    create_table()

    # Step 2: get a token from the API
    print("Requesting token...")
    token = get_token()

    if token is None:
        print("Could not retrieve token. Exiting.")
        return

    # Step 3: fetch all incidents from the API
    print("Fetching incidents...")
    incidents = fetch_incidents(token)
    print(f"Fetched {len(incidents)} incidents")

    # Step 3.5: save the raw incident data to a JSON file
    with open("incidents.json", "w") as f:
        json.dump(incidents, f, indent=4)
    print("Incidents saved to incidents.json")

    # Step 4: loop through incidents and their alerts and store them
    print("Storing alerts in database...")
    alert_count = 0

    for incident in incidents:
        incident_id = incident.get("incidentId")

        for alert in incident.get("alerts", []):
            timestamp = datetime.now().isoformat()
            insert_alert(alert, incident_id, timestamp)
            alert_count += 1

    print(f"Done. {alert_count} alerts stored in incidents.db")


if __name__ == "__main__":
    main()