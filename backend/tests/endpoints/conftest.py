""" Configuration for pytest, Flask, and the test client."""

import tempfile
import os
from datetime import datetime
import pytest
from sqlalchemy import create_engine
from project import create_app_with_db
from project.db_in import url, db
from project.models.course import Course
from project.models.user import User
from project.models.project import Project
from project.models.course_relation import CourseStudent,CourseAdmin

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
    """A fixture that creates and configure a new app instance for each test.
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
def project(course):
    """A project for testing, with the course as the course it belongs to"""
    date = datetime(2024, 2, 25, 12, 0, 0)
    project = Project(
        title="Project",
        descriptions="Test project",
        course_id=course.course_id,
        assignment_file="testfile",
        deadline=date,
        visible_for_students=True,
        archieved=False,
        test_path="testpad",
        script_name="testscript",
        regex_expressions='r'
    )
    return project

@pytest.fixture
def project_json(project: Project):
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
def courses_get_db(db_with_course):
    """Database equipped for the get tests"""
    for x in range(3,10):
        course = Course(teacher="Bart", name="Sel" + str(x))
        db_with_course.add(course)
        db_with_course.commit()
        db_with_course.add(CourseAdmin(course_id=course.course_id,uid="Bart"))
        db_with_course.commit()
    course = db_with_course.query(Course).filter_by(name="Sel2").first()
    db_with_course.add(CourseAdmin(course_id=course.course_id,uid="Rien"))
    db_with_course.add_all(
        [CourseStudent(course_id=course.course_id, uid="student_sel2_" + str(i))
         for i in range(3)])
    db_with_course.commit()
    return db_with_course

@pytest.fixture
def db_with_course(courses_init_db):
    """A database with a course."""
    courses_init_db.add(Course(name="Sel2", teacher="Bart"))
    courses_init_db.commit()
    course = courses_init_db.query(Course).filter_by(name="Sel2").first()
    courses_init_db.add(CourseAdmin(course_id=course.course_id,uid="Bart"))
    courses_init_db.commit()
    return courses_init_db

@pytest.fixture
def course_data():
    """A valid course for testing."""
    return {"name": "Sel2", "teacher": "Bart"}

@pytest.fixture
def invalid_course():
    """An invalid course for testing."""
    return {"invalid": "error"}

@pytest.fixture
def courses_init_db(db_session, course_students, course_teacher, course_assistent):
    """
    What do we need to test the courses api standalone:
    A teacher that can make a new course
    and some students
    and an assistent
    """
    db_session.add_all(course_students)
    db_session.add(course_teacher)
    db_session.add(course_assistent)
    db_session.commit()
    return db_session

@pytest.fixture
def course_students():
    """A list of 5 students for testing."""
    students = [
        User(uid="student_sel2_" + str(i), is_teacher=False, is_admin=False)
        for i in range(5)
    ]
    return students

@pytest.fixture
def course_teacher():
    """A user that's a teacher for testing"""
    sel2_teacher = User(uid="Bart", is_teacher=True, is_admin=False)
    return sel2_teacher

@pytest.fixture
def course_assistent():
    """A user that's a teacher for testing"""
    sel2_assistent = User(uid="Rien", is_teacher=True, is_admin=False)
    return sel2_assistent

@pytest.fixture
def course(course_teacher):
    """A course for testing, with the course teacher as the teacher."""
    sel2 = Course(name="Sel2", teacher=course_teacher.uid)
    return sel2
