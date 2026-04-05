# Import functions from other modules (modular design)
from token_handler import get_token
from api_handler import get_incidents
from database import create_database, store_incidents

# Base API URL
BASE_URL = "http://164.92.167.24"

# Endpoints
TOKEN_URL = f"{BASE_URL}/api/auth/token"
INCIDENTS_URL = f"{BASE_URL}/api/incidents"

# Your email (used for authentication)
EMAIL = "sana1001@stud.ek.dk"

def main():

    print("\nGetting token...\n")

    # Step 1: Get authentication token
    token = get_token(TOKEN_URL, EMAIL)

    # If token failed → stop program
    if not token:
        print("Failed to get token\n")
        return

    print("Token received successfully!\n")

    print("Fetching incidents...\n")

    # Step 2: Fetch incidents from API
    data = get_incidents(INCIDENTS_URL, token)
    incidents = data.get("value", [])

    # If no incidents → stop program
    if not incidents:
        print("No incidents found\n")
        return

    print(f"Retrieved {len(incidents)} incidents\n")

    # Count total alerts across all incidents
    total_alerts = sum(len(i.get("alerts", [])) for i in incidents)

    print("Fetching alerts...\n")
    print(f"Retrieved {total_alerts} alerts\n")

    print("Creating database...\n")

    # Step 3: Create database/table
    create_database()

    print("Saving to database...")

    # Step 4: Store alerts in database
    stored_alerts = store_incidents(data)

    # Final output
    print(f"\nStored {len(incidents)} incidents and {stored_alerts} alerts in the database successfully!\n")

# Entry point of the program
# Ensures script runs only when executed directly (not when imported)
if __name__ == "__main__":
    main()