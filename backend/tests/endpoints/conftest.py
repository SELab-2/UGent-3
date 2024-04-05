"""Endpoint level fixtures"""

import tempfile
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Tuple, List

import pytest
from pytest import fixture, FixtureRequest
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from project.models.user import User,Role
from project.models.course import Course
from project.models.course_relation import CourseStudent, CourseAdmin
from project.models.course_share_code import CourseShareCode
from project.models.submission import Submission, SubmissionStatus
from project.models.project import Project

### AUTHENTICATION & AUTHORIZATION ###
@fixture
def auth_test(request: FixtureRequest, client: FlaskClient, course: Course) -> Tuple:
    """Add concrete test data"""
    # endpoint, parameters, method, token, status
    endpoint, parameters, method, *other = request.param

    d = {
        "course_id": course.course_id
    }

    for index, parameter in enumerate(parameters):
        endpoint = endpoint.replace(f"@{index}", str(d[parameter]))

    return endpoint, getattr(client, method), *other



### USERS ###
@fixture
def student(session: Session) -> User:
    """Return a student entry"""
    return session.get(User, "student")

@fixture
def student_other(session: Session) -> User:
    """Return a student entry"""
    return session.get(User, "student_other")

@fixture
def teacher(session: Session) -> User:
    """Return a teacher entry"""
    return session.get(User, "teacher")

@fixture
def admin(session: Session) -> User:
    """Return an admin entry"""
    return session.get(User, "admin")



### COURSES ###
@fixture
def courses(session: Session, teacher: User) -> List[Course]:
    """Return course entries"""
    courses = [Course(name=f"SEL{i}", teacher=teacher.uid) for i in range(1, 3)]
    session.add_all(courses)
    session.commit()
    return courses

@fixture
def course(session: Session, student: User, teacher: User, admin: User) -> Course:
    """Return a course entry"""
    course = Course(name="SEL", ufora_id="C003784A_2023", teacher=teacher.uid)
    session.add(course)
    session.commit()
    session.add(CourseStudent(course_id=course.course_id, uid=student.uid))
    session.add(CourseAdmin(course_id=course.course_id, uid=admin.uid))
    session.commit()
    return course



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
def valid_project(course):
    """A function that return the json form data of a project"""
    data = {
        "title": "Project",
        "description": "Test project",
        "assignment_file": "testfile",
        "deadline": "2024-02-25T12:00:00",
        "course_id": course.course_id,
        "visible_for_students": True,
        "archived": False,
        "test_path": "tests",
        "script_name": "script.sh",
        "regex_expressions": ["*.pdf", "*.txt"]
    }
    return data

@pytest.fixture
def course_no_name(teacher):
    """A course with no name"""
    return {"name": "", "teacher": teacher.uid}

@pytest.fixture
def course_empty_name():
    """A course with an empty name"""
    return {"name": "", "teacher": "Bart"}

@pytest.fixture
def invalid_course():
    """An invalid course for testing."""
    return {"invalid": "error"}

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
def share_code_admin(session, course):
    """A course with share codes for testing."""
    share_code = CourseShareCode(course_id=course.course_id, for_admins=True)
    session.add(share_code)
    session.commit()
    return share_code
