import requests  # Used to make HTTP requests

def get_token(token_url, email):

    try:
        # Send POST request to get authentication token
        response = requests.post(
            token_url,
            json={"email": email},  # JSON payload (converted automatically)
            timeout=5               # Prevent hanging
        )

        # Raise error if HTTP response is bad
        response.raise_for_status()

        # Convert JSON response to dictionary
        data = response.json()

        # Extract token from response
        token = data.get("token")

        # If token is missing → something went wrong
        if not token:
            print("No token received from API")
            return None

        return token  # Return valid token

    except requests.exceptions.Timeout:
        print("Request timed out while getting token")

    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)

    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

    return None  # Return None if anything fails