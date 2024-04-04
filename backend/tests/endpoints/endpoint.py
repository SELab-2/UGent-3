"""Base class for endpoint tests"""

from typing import List, Tuple
from pytest import param

def authentication_tests(tests: List[Tuple[str, List[str], List[str]]]) -> List[any]:
    """Transform the format to single authentication tests"""

    single_tests = []
    for test in tests:
        endpoint, parameters, methods = test
        for method in methods:
            single_tests.append(param(
                (endpoint, parameters, method),
                id = f"{endpoint} {method.upper()}"
            ))
    return single_tests

def authorization_tests(tests: List[Tuple[str, List[str], str, List[str], List[str]]]) -> List[any]:
    """Transform the format to single authorization tests"""

    single_tests = []
    for test in tests:
        endpoint, parameters, method, allowed_tokens, disallowed_tokens = test
        for token in (allowed_tokens + disallowed_tokens):
            allowed = token in allowed_tokens
            single_tests.append(param(
                (endpoint, parameters, method, token, allowed),
                id = f"{endpoint} {method.upper()} " \
                    f"({token} {'allowed' if allowed else 'disallowed'})"
            ))
    return single_tests

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
