""" Configuration for pytest, Flask, and the test client."""
import pytest
from project import create_app

@pytest.fixture
def app():
    """A fixture that creates and configure a new app instance for each test.
    Returns:
        Flask -- A Flask application instance
    """
    app = create_app() # pylint: disable=redefined-outer-name ; fixture testing requires the same name to be used
    yield app

@pytest.fixture
def client(app): # pylint: disable=redefined-outer-name ; fixture testing requires the same name to be used
    """A fixture that creates a test client for the app.
    Arguments:
        app {Flask} -- A Flask application instance
    Returns:
        Flask -- A Flask test client instance
    """
    return app.test_client()
