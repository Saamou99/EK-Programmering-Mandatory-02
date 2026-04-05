import requests  # Library used for making HTTP requests (API calls)

def get_incidents(incidents_url, token):

    # Authorization header required by API (Bearer token authentication)
    headers = {
        "Authorization": f"Bearer {token}"
    }

    all_incidents = []  # List to store ALL incidents across multiple pages
    skip = 0            # Pagination offset (how many incidents to skip)

    try:
        while True:  # Loop to fetch all pages of incidents

            # Send GET request to API
            response = requests.get(
                incidents_url,
                headers=headers,                      # Include authentication token
                params={"$top": 100, "$skip": skip},  # Pagination parameters
                timeout=5                             # Prevent hanging if server is slow
            )

            # Raises an error if response status is 4xx or 5xx
            response.raise_for_status()

            # Convert JSON response to Python dictionary
            data = response.json()

            # Extract incidents list from response
            incidents = data.get("value", [])

            # If no incidents returned → we reached last page → stop loop
            if not incidents:
                break

            # Add current page incidents to full list
            all_incidents.extend(incidents)

            # Move to next page (skip next 100)
            skip += 100

        # Return all incidents in same structure as API
        return {"value": all_incidents}

    # Handle timeout (server too slow / no response)
    except requests.exceptions.Timeout:
        print("Request timed out while fetching incidents")

    # Handle HTTP errors (401, 404, 500, etc.)
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)

    # Handle all other request-related errors (network issues, DNS, etc.)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

    # Return empty result if something failed (prevents crashes)
    return {"value": []}