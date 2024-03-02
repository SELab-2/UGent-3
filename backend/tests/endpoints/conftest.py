""" Configuration for pytest, Flask, and the test client."""
import os
from dotenv import load_dotenv
import flask
import pytest
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from project.models.course_relations import CourseAdmins, CourseStudents
from project.models.courses import Courses
from project.models.users import Users
from project import create_app_with_db, db

load_dotenv()

DATABSE_NAME = os.getenv('POSTGRES_DB')
DATABASE_USER = os.getenv('POSTGRES_USER')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_HOST = os.getenv('POSTGRES_HOST')

url = URL.create(
    drivername="postgresql",
    username=DATABASE_USER,
    host=DATABASE_HOST,
    database=DATABSE_NAME,
    password=DATABASE_PASSWORD
)

@pytest.fixture
def api_url():
    #temporary
    return "http://localhost"
    return os.getenv('API_HOST')

@pytest.fixture
def app():
    app = create_app_with_db(url)
    return app

@pytest.fixture
def client(app):
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
def courses_init_db(db_session,course_students,course_teacher,course_assistent):
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