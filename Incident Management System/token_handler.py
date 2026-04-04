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

        response.raise_for_status()

        data = response.json()
        token = data.get("token")

        if not token:
            print("No token received from API")
            return None

        print("Token received successfully")
        return token

    except requests.exceptions.Timeout:
        print("Request timed out")

    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
        print("Response:", response.text)  # 🔥 debugging bonus

    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

    return None