from token_handler import get_token
from api_handler import get_incidents
from database import create_database, store_incidents


BASE_URL = "http://164.92.167.24"

TOKEN_URL = f"{BASE_URL}/api/auth/token"
INCIDENTS_URL = f"{BASE_URL}/api/incidents"

EMAIL = "sana1001@stud.ek.dk"


def main():
    print("Getting token...")

    token = get_token(TOKEN_URL, EMAIL)

    if not token:
        print("Failed to get token")
        return

    print("Token received!\n")

    print("Fetching incidents...")

    data = get_incidents(INCIDENTS_URL, token)

    if not data:
        print("Failed to fetch incidents")
        return

    alerts = data.get("value", [])

    print(f"Retrieved {len(alerts)} incidents\n")

    print("Creating database...")
    create_database()

    print("Saving to database...")

    store_incidents(data)

    #print(f"Stored {len(alerts)} incidents")
    print("\nData stored successfully in Database!")

if __name__ == "__main__": #Making a file runnable as the entry point while allowing imports from other modules
    main()