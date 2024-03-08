import requests

url = "http://localhost:8080/introspect"
payload = {
    "token": "tokentokentoken",
    'token_type_hint': 'access_token'
}

# Make a POST request to the specified URL with the payload
response = requests.post(url, data=payload, auth=("myClientID", "secret"))

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the token received in the response
    print("Token:", response.json().get("token"))
else:
    # Print an error message if the request was not successful
    print("Error:", response.status_code, response.text)
