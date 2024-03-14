""" Configuration for pytest, Flask, and the test client."""

import tempfile
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from sqlalchemy import create_engine

from project.models.course import Course
from project.models.user import User
from project.models.project import Project
from project.models.course_relation import CourseStudent,CourseAdmin
from project.models.course_share_code import CourseShareCode
from project import create_app_with_db
from project.db_in import url, db
from project.models.submission import Submission


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
        "submission_status": True
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
        "is_teacher": False
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
        User(uid="del", is_admin=False, is_teacher=True),
        User(uid="pat", is_admin=False, is_teacher=True),
        User(uid="u_get", is_admin=False, is_teacher=True),
        User(uid="query_user", is_admin=True, is_teacher=False)]

    session.add_all(users)
    session.commit()

    return users

def users():
    """Return a list of users to populate the database"""
    return [
        User(uid="brinkmann", is_admin=True, is_teacher=True),
        User(uid="laermans", is_admin=True, is_teacher=True),
        User(uid="student01", is_admin=False, is_teacher=False),
        User(uid="student02", is_admin=False, is_teacher=False)
    ]

def courses():
    """Return a list of courses to populate the database"""
    return [
        Course(name="AD3", teacher="brinkmann"),
        Course(name="RAF", teacher="laermans"),
    ]

def course_relations(session):
    """Returns a list of course relations to populate the database"""
    course_id_ad3 = session.query(Course).filter_by(name="AD3").first().course_id
    course_id_raf = session.query(Course).filter_by(name="RAF").first().course_id

    return [
        CourseAdmin(course_id=course_id_ad3, uid="brinkmann"),
        CourseStudent(course_id=course_id_ad3, uid="student01"),
        CourseStudent(course_id=course_id_ad3, uid="student02"),
        CourseAdmin(course_id=course_id_raf, uid="laermans"),
        CourseStudent(course_id=course_id_raf, uid="student02")
    ]

def projects(session):
    """Return  a list of projects to populate the database"""
    course_id_ad3 = session.query(Course).filter_by(name="AD3").first().course_id
    course_id_raf = session.query(Course).filter_by(name="RAF").first().course_id

    return [
        Project(
            title="B+ Trees",
            description="Implement B+ trees",
            assignment_file="assignement.pdf",
            deadline=datetime(2024,3,15,13,0,0),
            course_id=course_id_ad3,
            visible_for_students=True,
            archived=False,
            test_path="/tests",
            script_name="script.sh",
            regex_expressions=["solution"]
        ),
        Project(
            title="Predicaten",
            description="Predicaten project",
            assignment_file="assignment.pdf",
            deadline=datetime(2023,3,15,13,0,0),
            course_id=course_id_raf,
            visible_for_students=False,
            archived=True,
            test_path="/tests",
            script_name="script.sh",
            regex_expressions=[".*"]
        )
    ]

def submissions(session):
    """Return a list of submissions to populate the database"""
    project_id_ad3 = session.query(Project).filter_by(title="B+ Trees").first().project_id
    project_id_raf = session.query(Project).filter_by(title="Predicaten").first().project_id

    return [
        Submission(
            uid="student01",
            project_id=project_id_ad3,
            grading=16,
            submission_time=datetime(2024,3,14,12,0,0,tzinfo=ZoneInfo("GMT")),
            submission_path="/submissions/1",
            submission_status=True
        ),
        Submission(
            uid="student02",
            project_id=project_id_ad3,
            submission_time=datetime(2024,3,14,23,59,59,tzinfo=ZoneInfo("GMT")),
            submission_path="/submissions/2",
            submission_status=False
        ),
        Submission(
            uid="student02",
            project_id=project_id_raf,
            grading=15,
            submission_time=datetime(2023,3,5,10,0,0,tzinfo=ZoneInfo("GMT")),
            submission_path="/submissions/3",
            submission_status=True
        )
    ]

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
def session(db_session):
    """Create a database session for the tests"""
    # Populate the database
    db_session.add_all(users())
    db_session.commit()
    db_session.add_all(courses())
    db_session.commit()
    db_session.add_all(course_relations(db_session))
    db_session.commit()
    db_session.add_all(projects(db_session))
    db_session.commit()
    db_session.add_all(submissions(db_session))
    db_session.commit()

    # Tests can now use a populated database
    yield db_session

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
    ad_teacher = User(uid="Gunnar", is_teacher=True, is_admin=True)
    return ad_teacher

@pytest.fixture
def course_ad(course_teacher_ad: User):
    """A course for testing, with the course teacher as the teacher."""
    ad2 = Course(name="Ad2", teacher=course_teacher_ad.uid)
    return ad2

@pytest.fixture
def valid_project_entry(session, valid_project, valid_course_entry):
    """A project for testing, with the course as the course it belongs to"""
    date = datetime(2024, 2, 25, 12, 0, 0)
    project = Project(
        title="Project",
        description="Test project",
        course_id=valid_course_entry.course_id,
        deadline=date,
        visible_for_students=True,
        archived=False,
        test_path="testpad",
        script_name="testscript",
        regex_expressions='r'
    )

    session.add(project)
    session.commit()
    return project

@pytest.fixture
def valid_project(valid_course_entry):
    """A function that return the json form data of a project"""
    data = {
        "title": "Project",
        "description": "Test project",
        "assignment_file": "testfile",
        "deadline": "2024-02-25T12:00:00",
        "course_id": valid_course_entry.course_id,
        "visible_for_students": True,
        "archived": False,
        "test_path": "tests",
        "script_name": "script.sh",
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
    teacher = User(uid="Bart", is_teacher=True)
    session.add(teacher)
    session.commit()
    return teacher

@pytest.fixture
def valid_course(valid_teacher_entry):
    """A valid course json form"""
    return {"name": "Sel", "teacher": valid_teacher_entry.uid}

@pytest.fixture
def course_no_name(valid_teacher_entry):
    """A course with no name"""
    return {"name": "", "teacher": valid_teacher_entry.uid}

@pytest.fixture
def valid_course_entry(session, valid_teacher_entry):
    """A valid course for testing that's already in the db"""
    course = Course(name="Sel", teacher=valid_teacher_entry.uid)
    session.add(course)
    session.commit()
    return course

@pytest.fixture
def valid_students_entries(session):
    """Valid students for testing that are already in the db"""
    students = [
        User(uid=f"student_sel2_{i}", is_teacher=False)
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
