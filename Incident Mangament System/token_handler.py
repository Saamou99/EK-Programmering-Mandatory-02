import requests

def get_token(token_url, email):
    """
    Get authentication token using email.
    """

    try:
        response = requests.post(
            token_url,
            json={"email": email},
            timeout=5
        )

        response.raise_for_status()  # catches 4xx / 5xx errors

        data = response.json()
        return data.get("token")

    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

    return None