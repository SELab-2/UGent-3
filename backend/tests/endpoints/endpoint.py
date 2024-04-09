"""Base class for endpoint tests"""

from typing import List, Tuple, Dict
from pytest import param

def authentication_tests(tests: List[Tuple[str, List[str]]]) -> List[any]:
    """Transform the format to single authentication tests"""

    single_tests = []
    for test in tests:
        endpoint, methods = test
        for method in methods:
            single_tests.append(param(
                (endpoint, method),
                id = f"{endpoint} {method.upper()}"
            ))
    return single_tests

def authorization_tests(tests: List[Tuple[str, str, List[str], List[str]]]) -> List[any]:
    """Transform the format to single authorization tests"""

    single_tests = []
    for test in tests:
        endpoint, method, allowed_tokens, disallowed_tokens = test
        for token in (allowed_tokens + disallowed_tokens):
            allowed = token in allowed_tokens
            single_tests.append(param(
                (endpoint, method, token, allowed),
                id = f"{endpoint} {method.upper()} " \
                    f"({token} {'allowed' if allowed else 'disallowed'})"
            ))
    return single_tests

def data_field_type_tests(
        tests: List[Tuple[str, str, str, Dict[str, any], Dict[str, List[any]]]]
    ) -> List[any]:
    """Transform the format to single data_field tests"""

    single_tests = []
    for test in tests:
        endpoint, method, token, data, changes = test

        # Test by adding an incorrect field
        new_data = dict(data)
        new_data["field"] = None
        single_tests.append(param(
            (endpoint, method, token, new_data),
            id = f"{endpoint} {method.upper()} {token} (field None 400)"
        ))

        # Test the with the given changes
        for key, values in changes.items():
            for value in values:
                new_data = dict(data)
                new_data[key] = value
                single_tests.append(param(
                    (endpoint, method, token, new_data),
                    id = f"{endpoint} {method.upper()} {token} ({key} {value} 400)"
                ))
    return single_tests

class TestEndpoint:
    """Base class for endpoint tests"""

    def authentication(self, auth_test: Tuple[str, any]):
        """Test if the authentication for the given enpoint works"""

        endpoint, method = auth_test

        response = method(endpoint)
        assert response.status_code == 401

        response = method(endpoint, headers = {"Authorization": "0123456789"})
        assert response.status_code == 401

        response = method(endpoint, headers = {"Authorization": "login"})
        assert response.status_code != 401

    def authorization(self, auth_test: Tuple[str, any, str, bool]):
        """Test if the authorization for the given endpoint works"""

        endpoint, method, token, allowed = auth_test

        response = method(endpoint, headers = {"Authorization": token})
        assert allowed == (response.status_code != 403)

    def data_field_type(self, data_field_test: Tuple[str, any, str, Dict[str, any]]):
        """Test if the datatypes are properly checked for data fields"""

        endpoint, method, token, data = data_field_test

        response = method(endpoint, headers = {"Authorization": token}, json = data)
        assert response.status_code == 400
