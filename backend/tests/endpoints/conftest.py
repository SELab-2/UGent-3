""" Configuration for pytest, Flask, and the test client."""
import pytest
from project import create_app_with_db
from project.database import db, get_database_uri

@pytest.fixture
def session():
    """Create a database session for the tests"""
    # Create all tables
    db.create_all()

    # Populate the database
    db.session.commit()

    # Tests can now use a populated database
    yield db.session

    # Rollback
    db.session.rollback()

    # Remove all tables
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

    db.session.close()

@pytest.fixture
def app():
    """A fixture that creates and configure a new app instance for each test.
    Returns:
        Flask -- A Flask application instance
    """
    app = create_app_with_db(get_database_uri())
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
