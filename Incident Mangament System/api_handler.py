import requests

def get_incidents(api_url, token):
    """
    Fetch incidents from API.
    """

    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(api_url, headers=headers, timeout=5)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

    return None