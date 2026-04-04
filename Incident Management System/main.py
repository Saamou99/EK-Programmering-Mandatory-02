from token_handler import get_token
from api_handler import get_incidents
from database import create_database, store_incidents

BASE_URL = "http://164.92.167.24"

TOKEN_URL = f"{BASE_URL}/api/auth/token"
INCIDENTS_URL = f"{BASE_URL}/api/incidents"

EMAIL = "sana1001@stud.ek.dk"


def main():

    print("\nGetting token...\n")

    token = get_token(TOKEN_URL, EMAIL)

    if not token:
        print("Failed to get token\n")
        return

    print("Token received successfully!\n")

    print("Fetching incidents...\n")

    data = get_incidents(INCIDENTS_URL, token)
    incidents = data.get("value", [])

    if not incidents:
        print("No incidents found\n")
        return

    print(f"Retrieved {len(incidents)} incidents\n")

    # 🔥 Count alerts BEFORE saving
    total_alerts = sum(len(i.get("alerts", [])) for i in incidents)

    print("Fetching alerts...\n")
    print(f"Retrieved {total_alerts} alerts\n")

    print("Creating database...\n")
    create_database()

    print("Saving to database...")
    stored_alerts = store_incidents(data)

    print(f"\nStored {len(incidents)} incidents and {stored_alerts} alerts in the database successfully!\n")

if __name__ == "__main__":
    main()