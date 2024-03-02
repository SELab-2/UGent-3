"""Configuration for pytest, Flask, and the test client."""

import os
import pytest
from project.models.courses import Courses
from project.models.users import Users
from project.models.course_relations import CourseStudents,CourseAdmins
from project import create_app_with_db, db
from project.db_in import url


@pytest.fixture
def api_url():
    """Get the API URL from the environment."""
    return os.getenv("API_HOST")


@pytest.fixture
def app():
    """Get the app"""
    app = create_app_with_db(url)
    return app


@pytest.fixture
def client(app):
    """Returns client for testing requests to the app."""
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def db_session(app):
    """Create a new database session for a test.
    After the test, all changes are rolled back and the session is closed."""
    app = create_app_with_db(url)
    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        yield db.session
        db.session.close()

@pytest.fixture
def courses_get_db(db_with_course):
    """Database equiped for the get tests"""
    for x in range(3,10):
        course = Courses(teacher="Bart", name="Sel" + str(x))
        db_with_course.add(course)
        db_with_course.commit()
        db_with_course.add(CourseAdmins(course_id=course.course_id,uid="Bart"))
        db_with_course.commit()
    course = db_with_course.query(Courses).filter_by(name="Sel2").first()
    db_with_course.add(CourseAdmins(course_id=course.course_id,uid="Rien"))
    db_with_course.add_all(
        [CourseStudents(course_id=course.course_id, uid="student_sel2_" + str(i))
         for i in range(3)])
    db_with_course.commit()
    return db_with_course

@pytest.fixture
def db_with_course(courses_init_db):
    """A database with a course."""
    courses_init_db.add(Courses(name="Sel2", teacher="Bart"))
    courses_init_db.commit()
    course = courses_init_db.query(Courses).filter_by(name="Sel2").first()
    courses_init_db.add(CourseAdmins(course_id=course.course_id,uid="Bart"))
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
        Users(uid="student_sel2_" + str(i), is_teacher=False, is_admin=False)
        for i in range(5)
    ]
    return students


@pytest.fixture
def course_teacher():
    """A user that's a teacher for for testing"""
    sel2_teacher = Users(uid="Bart", is_teacher=True, is_admin=False)
    return sel2_teacher


@pytest.fixture
def course_assistent():
    """A user that's a teacher for for testing"""
    sel2_assistent = Users(uid="Rien", is_teacher=True, is_admin=False)
    return sel2_assistent


@pytest.fixture
def course(course_teacher):
    """A course for testing, with the course teacher as the teacher."""
    sel2 = Courses(name="Sel2", teacher=course_teacher.uid)
    return sel2
