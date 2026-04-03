import requests

def get_incidents(incidents_url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    all_incidents = []
    skip = 0

    try:
        while True:
            response = requests.get(
                incidents_url,
                headers=headers,
                params={"$top": 100, "$skip": skip},
                timeout=5  # prevent hanging
            )

            # Raise error for bad status codes (4xx, 5xx)
            response.raise_for_status()

            data = response.json()
            incidents = data.get("value", [])

            # Stop if no more data
            if not incidents:
                break

            # Add incidents to list
            all_incidents.extend(incidents)

            # Move to next page
            skip += 100

        return {"value": all_incidents}

    # Specific timeout error
    except requests.exceptions.Timeout:
        print("Request timed out while fetching incidents")

    # HTTP error (like 404, 500)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")

    # Any other request-related error
    except requests.exceptions.RequestException as e:
        print(f"General request error: {e}")

    return {"value": []}  # return empty list on failure