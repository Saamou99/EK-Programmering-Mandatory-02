import requests
import time

BASE_URL = "http://164.92.167.24"
EMAIL = "cph-cg193@stud.ek.dk"


def get_token():
    """Request a fresh token from the API using our school email."""
    try:
        url = f"{BASE_URL}/api/auth/token"
        response = requests.post(url, json={"email": EMAIL})
        response.raise_for_status()
        data = response.json()
        return data["token"]
    except requests.exceptions.Timeout:
        print("Error: request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: something went wrong: {e}")


def fetch_incidents(token):
    """Fetch all incidents from the API using pagination."""
    headers = {"Authorization": f"Bearer {token}"}
    all_incidents = []
    skip = 0

    while True:
        try:
            response = requests.get(f"{BASE_URL}/api/incidents", headers=headers, params={"$top": 100, "$skip": skip})
            response.raise_for_status()
            data = response.json()
            incidents = data["value"]
            # Use extend instead of append as append would add the whole list instead of individual incidents
            all_incidents.extend(incidents)

            if "@odata.nextLink" not in data:
                break
            skip += 100
            time.sleep(1.5)
        except requests.exceptions.Timeout:
            print("Error: request timed out")
            break
        except requests.exceptions.HTTPError as e:
            print(f"Error: HTTP error occurred: {e}")
            break
        except requests.exceptions.RequestException as e:
            print(f"Error: something went wrong: {e}")
            break

    return all_incidents