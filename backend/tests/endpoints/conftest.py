""" Configuration for pytest, Flask, and the test client."""
from datetime import datetime
from os import getenv
from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from project import create_app_with_db, db
from project.models.users import Users
from project.models.courses import Courses
from project.models.projects import Projects

load_dotenv()

url = URL.create(
    drivername="postgresql",
    username=getenv("POSTGRES_USER"),
    password=getenv("POSTGRES_PASSWORD"),
    host=getenv("POSTGRES_HOST"),
    database=getenv("POSTGRES_DB")
)


@pytest.fixture
def course_teacher():
    """A user that's a teacher for for testing"""
    ad_teacher = Users(uid="Gunnar", is_teacher=True, is_admin=True)
    print("teacher")
    print(ad_teacher)
    return ad_teacher


@pytest.fixture
def course(course_teacher: Users):
    """A course for testing, with the course teacher as the teacher."""
    print("teacher id")
    print(course_teacher.uid)
    ad2 = Courses(name="Ad2", teacher=course_teacher.uid)
    return ad2


@pytest.fixture
def project(course):
    """A project for testing, with the course as the course it belongs to"""
    date = datetime(2024, 2, 25, 12, 0, 0)
    project = Projects(
        title="Project",
        descriptions="Test project",
        course_id=course.course_id,
        deadline=date,
        visible_for_students=True,
        archieved=False,
    )
    return project

@pytest.fixture
def project_json(project: Projects):
    """A function that return the json data of a project including the PK neede for testing"""
    data = {
        "title": project.title,
        "descriptions": project.descriptions,
        "assignment_file": project.assignment_file,
        "deadline": project.deadline,
        "course_id": project.course_id,
        "visible_for_students": project.visible_for_students,
        "archieved": project.archieved,
        "test_path": project.test_path,
        "script_name": project.script_name,
        "regex_expressions": project.regex_expressions
    }
    return data


@pytest.fixture
def app():
    """A fixture that creates and configure a new app instance for each test.
    Returns:
        Flask -- A Flask application instance
    """
    load_dotenv()

    db_url = URL.create(
        drivername="postgresql",
        username=getenv("POSTGRES_USER"),
        password=getenv("POSTGRES_PASSWORD"),
        host=getenv("POSTGRES_HOST"),
        database=getenv("POSTGRES_DB")
    )
    engine = create_engine(db_url)
    # Session = sessionmaker(bind=engine)
    app = create_app_with_db(db_url)
    db.metadata.create_all(engine)
    yield app


engine = create_engine(url)
Session = sessionmaker(bind=engine)


@pytest.fixture
def db_session():
    """Create a new database session for a test.
    After the test, all changes are rolled back and the session is closed."""
    db.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
    # Truncate all tables
    for table in reversed(db.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


@pytest.fixture
def client(app):
    """A fixture that creates a test client for the app.
    Arguments:
        app {Flask} -- A Flask application instance
    Returns:
        Flask -- A Flask test client instance
    """
    return app.test_client()
