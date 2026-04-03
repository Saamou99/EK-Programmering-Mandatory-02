import requests

def get_token(token_url, email):        #Get authentication token using email
  
    try:
        response = requests.post(       #POST method || request method use json module internally
            token_url,
            json={"email": email},      #Payload format
            timeout=5                   #Timeout important for real systems
        )

        response.raise_for_status()     #Error handling for 400/401/500 errors

        data = response.json()
        token = data.get("token")

        if not token:
            print("No token received from API")
            return None
        
        return token

    except requests.exceptions.Timeout:
        print("Request timed out")

    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
        print("Response:", response.text)  

    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

    return None