""" Configuration for pytest, Flask, and the test client."""
from os import getenv

import pytest
from project import create_app, create_app_with_db
from dotenv import load_dotenv

@pytest.fixture
def app():
    """A fixture that creates and configure a new app instance for each test.
    Returns:
        Flask -- A Flask application instance
    """
    load_dotenv()
    app = create_app_with_db(getenv("DB_HOST"))
    yield app

@pytest.fixture
def client(app):
    """A fixture that creates a test client for the app.
    Arguments:
        app {Flask} -- A Flask application instance
    Returns:
        Flask -- A Flask test client instance
    """
    return app.test_client()
