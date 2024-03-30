"""Base class for endpoint tests"""

from typing import List, Tuple
from pytest import param

class AuthenticationTests:
    """Class to create authentication tests"""

    def __init__(self):
        self.tests = []

    def add(self, endpoint: str, parameters: List[str], methods: List[str]):
        """Add authentication tests"""

        for method in methods:
            self.tests.append(param(
                (endpoint, parameters, method),
                id = f"{endpoint} {method}"
            ))

class AuhtorizationTests:
    """Class to create authorization tests"""

    def __init__(self):
        self.tests = []

    # Disable too many arguments warning
    # pylint: disable = R0913
    def add(self, endpoint: str, parameters: List[str], method: str,
            allowed_tokens: List[str], disallowed_tokens: List[str]):
        """Add authorization tests"""

        for token in (allowed_tokens + disallowed_tokens):
            allowed = token in allowed_tokens
            self.tests.append(param(
                (endpoint, parameters, method, token, allowed),
                id = f"{endpoint} {method} {token} {'allowed' if allowed else 'disallowed'}"
            ))

class TestEndpoint:
    """Base class for endpoint tests"""

    def authentication(self, authentication_parameter: Tuple[str, any]):
        """Test if the authentication for the given enpoint works"""

        endpoint, method = authentication_parameter

        response = method(endpoint)
        assert response.status_code == 401

        response = method(endpoint, headers = {"Authorization": "0123456789"})
        assert response.status_code == 401

        response = method(endpoint, headers = {"Authorization": "login"})
        assert response.status_code != 401

    def authorization(self, auth_parameter: Tuple[str, any, str, bool]):
        """Test if the authorization for the given endpoint works"""

        endpoint, method, token, allowed = auth_parameter

        response = method(endpoint, headers = {"Authorization": token})
        assert allowed == (response.status_code != 403)
