"""This file contains fixtures that are needed for most of the tests."""
import pytest
from project.db_in import url
from project import db
from project import create_app_with_db

@pytest.fixture
def app():
    """Get the app"""
    app = create_app_with_db(url)
    return app

@pytest.fixture
def db_session(app):
    """Create a new database session for a test.
    After the test, all changes are rolled back and the session is closed."""
    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        yield db.session
        db.session.close()
