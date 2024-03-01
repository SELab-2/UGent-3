""" Configuration for pytest, Flask, and the test client."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project import create_app_with_db
from project.database import db, get_database_uri

engine = create_engine(get_database_uri())
Session = sessionmaker(bind=engine)
@pytest.fixture
def session():
    """Create a database session for the tests"""
    # Create all tables
    db.metadata.create_all(engine)

    session = Session()

    # Populate the database
    session.commit()

    # Tests can now use a populated database
    yield session

    # Rollback
    session.rollback()
    session.close()

    # Remove all tables
    for table in reversed(db.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

@pytest.fixture
def app():
    """A fixture that creates and configure a new app instance for each test.
    Returns:
        Flask -- A Flask application instance
    """
    engine = create_engine(get_database_uri())
    app = create_app_with_db(get_database_uri())
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
