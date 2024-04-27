"""A file for utility functions to help handling the authentication in tests"""

def get_csrf_from_login(client, code):
    """Log the user in, adding the access token cookie and
    return the csrf token cookie to be used in the requests
    """
    response = client.get(f"/auth?code={code}")
    csrf = next((cookie for cookie
                in response.headers.getlist('Set-Cookie')
                if 'csrf_access_token' in cookie), "").split(";")[0].split("=")[1]
    return csrf
