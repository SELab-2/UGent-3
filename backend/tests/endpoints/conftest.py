""" Configuration for pytest, Flask, and the test client."""
import pytest
from sqlalchemy import create_engine
from project import create_app_with_db
from project import db
from tests import db_url



@pytest.fixture
def app():
    """A fixture that creates and configure a new app instance for each test.
    Returns:
        Flask -- A Flask application instance
    """
    engine = create_engine(db_url)
    app = create_app_with_db(db_url)
    db.metadata.create_all(engine)
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
