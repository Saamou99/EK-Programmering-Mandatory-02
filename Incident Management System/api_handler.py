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
                timeout=5
            )

            response.raise_for_status()

            data = response.json()
            incidents = data.get("value", [])

            if not incidents:
                break

            all_incidents.extend(incidents)
            skip += 100

        return {"value": all_incidents}

    except requests.exceptions.Timeout:
        print("Request timed out while fetching incidents")

    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)

    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

    return {"value": []}