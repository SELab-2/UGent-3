"""
Configuration for the models tests. Contains all the fixtures needed for multiple models tests.
"""

import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import pytest
from project import db
from project.models.courses import Courses
from project.models.course_relations import CourseAdmins, CourseStudents
from project.models.projects import Projects
from project.models.users import Users

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

engine = create_engine(url)
Session = sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    """Create a new database session for a test.
    After the test, all changes are rolled back and the session is closed."""
    db.metadata.create_all(engine)
    session = Session()
    for table in reversed(db.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    yield session
    session.rollback()
    session.close()
    # Truncate all tables
    for table in reversed(db.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

@pytest.fixture
def valid_user():
    """A valid user for testing"""
    user = Users(uid="student", is_teacher=False, is_admin=False)
    return user

@pytest.fixture
def teachers():
    """A list of 10 teachers for testing"""
    users = [Users(uid=str(i), is_teacher=True, is_admin=False) for i in range(10)]
    return users

@pytest.fixture
def course_teacher():
    """A user that's a teacher for for testing"""
    sel2_teacher = Users(uid="Bart", is_teacher=True, is_admin=False)
    return sel2_teacher

@pytest.fixture
def course(course_teacher):
    """A course for testing, with the course teacher as the teacher."""
    sel2 = Courses(name="Sel2", teacher=course_teacher.uid)
    return sel2

@pytest.fixture
def course_students():
    """A list of 5 students for testing."""
    students = [
        Users(uid="student_sel2_" + str(i), is_teacher=False, is_admin=False)
            for i in range(5)
    ]
    return students

@pytest.fixture
def course_students_relation(course,course_students):
    """A list of 5 course relations for testing."""
    course_relations = [
        CourseStudents(course_id=course.course_id, uid=course_students[i].uid)
            for i in range(5)
    ]
    return course_relations

@pytest.fixture
def assistent():
    """An assistent for testing."""
    assist = Users(uid="assistent_sel2")
    return assist

@pytest.fixture()
def course_admin(course,assistent):
    """A course admin for testing."""
    admin_relation = CourseAdmins(uid=assistent.uid, course_id=course.course_id)
    return admin_relation

@pytest.fixture()
def valid_project():
    """A valid project for testing."""
    deadline = datetime(2024, 2, 25, 12, 0, 0)  # February 25, 2024, 12:00 PM
    project = Projects(
        title="Project",
        descriptions="Test project",
        deadline=deadline,
        visible_for_students=True,
        archieved=False,
    )
    return project
