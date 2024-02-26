""" Configuration for pytest, Flask, and the test client."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project import create_app_with_db
from project import db
from project.models.users import Users
from tests import db_url


engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
@pytest.fixture
def user_db_session():
    """Create a new database session for the user tests.
    After the test, all changes are rolled back and the session is closed."""
    db.metadata.create_all(engine)
    session = Session()
    session.add_all(
            [Users(uid="del", is_admin=False, is_teacher=True),
             Users(uid="pat", is_admin=False, is_teacher=True),
             Users(uid="u_get", is_admin=False, is_teacher=True)
             ]
        )
    session.commit()
    yield session
    session.rollback()
    session.close()
    # Truncate all tables
    for table in reversed(db.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


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
