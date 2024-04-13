""" Configuration for pytest, Flask, and the test client."""

import tempfile
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from pytest import fixture, FixtureRequest
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from project.models.user import User,Role
from project.models.course import Course
from project.models.course_share_code import CourseShareCode
from project import create_app_with_db
from project.db_in import url, db
from project.models.submission import Submission, SubmissionStatus
from project.models.project import Project

### AUTHENTICATION & AUTHORIZATION ###
@fixture
def auth_test(request: FixtureRequest, client: FlaskClient, valid_course_entry):
    """Add concrete test data"""
    # endpoint, parameters, method, token, status
    endpoint, parameters, method, *other = request.param

    d = {
        "course_id": valid_course_entry.course_id
    }

    for index, parameter in enumerate(parameters):
        endpoint = endpoint.replace(f"@{index}", str(d[parameter]))

    return endpoint, getattr(client, method), *other

### OTHER ###
@pytest.fixture
def valid_submission(valid_user_entry, valid_project_entry):
    """
    Returns a valid submission form
    """
    return {
        "uid": valid_user_entry.uid,
        "project_id": valid_project_entry.project_id,
        "grading": 16,
        "submission_time": datetime(2024,3,14,12,0,0,tzinfo=ZoneInfo("GMT")),
        "submission_path": "/submission/1",
        "submission_status": SubmissionStatus.SUCCESS
    }

@pytest.fixture
def valid_submission_entry(session, valid_submission):
    """
    Returns a submission that is in the database
    """
    submission = Submission(**valid_submission)
    session.add(submission)
    session.commit()
    return submission

@pytest.fixture
def valid_user():
    """
    Returns a valid user form
    """
    return {
        "uid": "w_student",
        "role": Role.STUDENT.name
    }

@pytest.fixture
def valid_user_entry(session, valid_user):
    """
    Returns a user that is in the database
    """
    user = User(**valid_user)
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def valid_admin():
    """
    Returns a valid admin user form
    """
    return {
        "uid": "admin_person",
        "role": Role.ADMIN,
    }

@pytest.fixture
def valid_admin_entry(session, valid_admin):
    """
    Returns an admin user that is in the database
    """
    user = User(**valid_admin)
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def user_invalid_field(valid_user):
    """
    Returns a user form with an invalid field
    """
    valid_user["is_student"] = True
    return valid_user

@pytest.fixture
def valid_user_entries(session):
    """
    Returns a list of users that are in the database
    """
    users = [
        User(uid="del", role=Role.TEACHER),
        User(uid="pat", role=Role.TEACHER),
        User(uid="u_get", role=Role.TEACHER),
        User(uid="query_user", role=Role.ADMIN)]

    session.add_all(users)
    session.commit()

    return users


@pytest.fixture
def file_empty():
    """Return an empty file"""
    descriptor, name = tempfile.mkstemp()
    with open(descriptor, "rb") as temp:
        yield temp, name

@pytest.fixture
def file_no_name():
    """Return a file with no name"""
    descriptor, name = tempfile.mkstemp()
    with open(descriptor, "w", encoding="UTF-8") as temp:
        temp.write("This is a test file.")
    with open(name, "rb") as temp:
        yield temp, ""

@pytest.fixture
def files():
    """Return a temporary file"""
    descriptor01, name01 = tempfile.mkstemp()
    with open(descriptor01, "w", encoding="UTF-8") as temp:
        temp.write("This is a test file.")
    descriptor02, name02 = tempfile.mkstemp()
    with open(descriptor02, "w", encoding="UTF-8") as temp:
        temp.write("This is a test file.")
    with open(name01, "rb") as temp01:
        with open(name02, "rb") as temp02:
            yield [(temp01, name01), (temp02, name02)]

@pytest.fixture
def app():
    """A fixture that creates and configures a new app instance for each test.
    Returns:
        Flask -- A Flask application instance
    """
    engine = create_engine(url)
    app = create_app_with_db(url)
    db.metadata.create_all(engine)
    yield app

@pytest.fixture
def course_teacher_ad():
    """A user that's a teacher for testing"""
    ad_teacher = User(uid="Gunnar", role=Role.TEACHER)
    return ad_teacher

@pytest.fixture
def course_ad(course_teacher_ad: User):
    """A course for testing, with the course teacher as the teacher."""
    ad2 = Course(name="Ad2", teacher=course_teacher_ad.uid)
    return ad2

@pytest.fixture
def valid_project_entry(session, valid_project):
    """A project for testing, with the course as the course it belongs to"""
    project = Project(**valid_project)

    session.add(project)
    session.commit()
    return project

@pytest.fixture
def valid_project(valid_course_entry):
    """A function that return the json form data of a project"""
    data = {
        "title": "Project",
        "description": "Test project",
        "deadlines": [{"deadline": "2024-02-25T12:00:00", "description": "Deadline 1"}],
        "course_id": valid_course_entry.course_id,
        "visible_for_students": True,
        "archived": False,
        "regex_expressions": ["*.pdf", "*.txt"]
    }
    return data

@pytest.fixture
def api_url():
    """Get the API URL from the environment."""
    return os.getenv("API_HOST")

@pytest.fixture
def client(app):
    """Returns client for testing requests to the app."""
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def valid_teacher_entry(session):
    """A valid teacher for testing that's already in the db"""
    teacher = User(uid="Bart", role=Role.TEACHER)
    try:
        session.add(teacher)
        session.commit()
    except SQLAlchemyError:
        session.rollback()
    return teacher

@pytest.fixture
def course_invalid_field(valid_course):
    """A course with an invalid field"""
    valid_course["test_field"] = "test_value"
    return valid_course

@pytest.fixture
def valid_course(valid_teacher_entry):
    """A valid course json form"""
    return {"name": "Sel", "teacher": valid_teacher_entry.uid}

@pytest.fixture
def course_no_name(valid_teacher_entry):
    """A course with no name"""
    return {"name": "", "teacher": valid_teacher_entry.uid}

@pytest.fixture
def course_empty_name():
    """A course with an empty name"""
    return {"name": "", "teacher": "Bart"}

@pytest.fixture
def invalid_course():
    """An invalid course for testing."""
    return {"invalid": "error"}

@pytest.fixture
def valid_course_entry(session, valid_course):
    """A valid course for testing that's already in the db"""
    course = Course(**valid_course)
    session.add(course)
    session.commit()
    return course

@pytest.fixture
def valid_students_entries(session):
    """Valid students for testing that are already in the db"""
    students = [
        User(uid=f"student_sel2_{i}", role=Role.STUDENT)
        for i in range(3)
    ]
    session.add_all(students)
    session.commit()
    return students

@pytest.fixture
def valid_course_entries(session, valid_teacher_entry):
    """A valid course for testing that's already in the db"""
    courses = [Course(name=f"Sel{i}", teacher=valid_teacher_entry.uid) for i in range(3)]
    session.add_all(courses)
    session.commit()
    return courses

@pytest.fixture
def share_code_admin(session, valid_course_entry):
    """A course with share codes for testing."""
    share_code = CourseShareCode(course_id=valid_course_entry.course_id, for_admins=True)
    session.add(share_code)
    session.commit()
    return share_code
