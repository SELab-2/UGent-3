""" Configuration for pytest, Flask, and the test client."""

from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project import create_app_with_db
from project.database import db, get_database_uri
from project.models.users import Users as m_users
from project.models.courses import Courses as m_courses
from project.models.course_relations import CourseAdmins as m_course_admins
from project.models.course_relations import CourseStudents as m_course_students
from project.models.projects import Projects as m_projects
from project.models.submissions import Submissions as m_submissions

@pytest.fixture
def users():
    """Return a list of users to populate the database"""
    return [
        m_users(uid="brinkmann", is_admin=True, is_teacher=True),
        m_users(uid="laermans", is_admin=True, is_teacher=True),
        m_users(uid="student01", is_admin=False, is_teacher=False),
        m_users(uid="student02", is_admin=False, is_teacher=False)
    ]

@pytest.fixture
def courses():
    """Return a list of courses to populate the database"""
    return [
        m_courses(course_id=1, name="AD3", teacher="brinkmann"),
        m_courses(course_id=2, name="RAF", teacher="laermans"),
    ]

@pytest.fixture
def course_relations():
    """Returns a list of course relations to populate the database"""
    return [
        m_course_admins(course_id=1, uid="brinkmann"),
        m_course_students(course_id=1, uid="student01"),
        m_course_students(course_id=1, uid="student02"),
        m_course_admins(course_id=2, uid="laermans"),
        m_course_students(course_id=2, uid="student02")
    ]

@pytest.fixture
def projects():
    """Return  a list of projects to populate the database"""
    return [
        m_projects(
            project_id=1,
            title="B+ Trees",
            descriptions="Implement B+ trees",
            assignment_file="assignement.pdf",
            deadline=datetime(2024,3,15,13,0,0),
            course_id=1,
            visible_for_students=True,
            archieved=False,
            test_path="/tests",
            script_name="script.sh",
            regex_expressions=["*"]
        ),
        m_projects(
            project_id=2,
            title="Predicaten",
            descriptions="Predicaten project",
            assignment_file="assignment.pdf",
            deadline=datetime(2023,3,15,13,0,0),
            course_id=2,
            visible_for_students=False,
            archieved=True,
            test_path="/tests",
            script_name="script.sh",
            regex_expressions=["*"]
        )
    ]

@pytest.fixture
def submissions():
    """Return a list of submissions to populate the database"""
    return [
        m_submissions(
            submission_id=1,
            uid="student01",
            project_id=1,
            grading=16,
            submission_time=datetime(2024,3,14,12,0,0),
            submission_path="/submissions/1",
            submission_status=True
        ),
        m_submissions(
            submission_id=2,
            uid="student02",
            project_id=1,
            submission_time=datetime(2024,3,14,23,59,59),
            submission_path="/submissions/2",
            submission_status=False
        ),
        m_submissions(
            submission_id=3,
            uid="student02",
            project_id=2,
            grading=15,
            submission_time=datetime(2023,3,5,10,0,0),
            submission_path="/submissions/3",
            submission_status=True
        )
    ]

engine = create_engine(get_database_uri())
Session = sessionmaker(bind=engine)
@pytest.fixture
def session(users,courses,course_relations,projects,submissions):
    """Create a database session for the tests"""
    # Create all tables and get a session
    db.metadata.create_all(engine)
    session = Session()

    try:
        # Populate the database
        session.add_all(users)
        session.commit()
        session.add_all(courses)
        session.commit()
        session.add_all(course_relations)
        session.commit()
        session.add_all(projects)
        session.commit()
        session.add_all(submissions)
        session.commit()

        # Tests can now use a populated database
        yield session
    finally:
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
