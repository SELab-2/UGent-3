"""root level fixtures"""
import pytest
from project.sessionmaker import engine, Session
from project.db_in import db

@pytest.fixture
def db_session():
    """Create a new database session for a test.
    After the test, all changes are rolled back and the session is closed."""

    db.metadata.create_all(engine)
    session = Session()

    try:
        yield session
    finally:
        # Rollback
        session.rollback()
        session.close()

        # Truncate all tables
        for table in reversed(db.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
