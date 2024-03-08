from authlib.oauth2.rfc7662 import IntrospectTokenValidator
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class UGentOAuthTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token_string):
        url = 'https://login.ugent.be/oauth2/introspect'
        data = {
            'token': token_string,
            'token_type_hint': 'access_token'
        }
        auth = (getenv("OAUTH_CLIENT_ID"), getenv("OAUTH_CLIENT_SECRET"))
        resp = requests.post(url, data, auth=auth)
        if resp.status_code != 200:
            return None
        return resp.json()
