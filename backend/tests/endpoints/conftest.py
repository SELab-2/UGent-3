""" Configuration for pytest, Flask, and the test client."""
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import URL
import pytest
from project import create_app_with_db

@pytest.fixture
def app():
    """A fixture that creates and configure a new app instance for each test.
    Returns:
        Flask -- A Flask application instance
    """
    load_dotenv()

    url = URL.create(
        drivername="postgresql",
        username=getenv("POSTGRES_USER"),
        password=getenv("POSTGRES_PASSWORD"),
        host=getenv("POSTGRES_HOST"),
        database=getenv("POSTGRES_DB")
    )
    app = create_app_with_db(url)
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
