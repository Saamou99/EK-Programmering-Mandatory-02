import requests

def get_incidents(api_url, token):
    """
    Fetch ALL incidents using pagination.
    """

    headers = {
        "Authorization": f"Bearer {token}"
    }

    all_incidents = []   # 👈 HERE (inside function)
    skip = 0

    try:
        while True:
            response = requests.get(
                api_url,
                headers=headers,
                params={"$top": 100, "$skip": skip},
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            # Get incidents batch
            batch = data.get("value", [])

            # Stop when no more data
            if not batch:
                break

            all_incidents.extend(batch)

            skip += 100  # Move to next page

        return {"value": all_incidents}

    except requests.exceptions.RequestException as e:
        print("API error:", e)
        return None