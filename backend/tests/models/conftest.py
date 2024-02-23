"""

"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from project import db
from project.models.courses import Courses
from project.models.course_relations import CourseAdmins, CourseStudents
from project.models.projects import Projects
from project.models.submissions import Submissions
from project.models.users import Users
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import pytest

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
def valid_user():
    user = Users(uid="student", is_teacher=False, is_admin=False)
    return user 

@pytest.fixture
def teachers():
    users = [Users(uid=str(i), is_teacher=True, is_admin=False) for i in range(10)]
    return users

@pytest.fixture
def course_teacher():
    sel2_teacher = Users(uid="Bart", is_teacher=True, is_admin=False)
    return sel2_teacher
        
@pytest.fixture
def course(course_teacher):
    sel2 = Courses(name="Sel2", teacher=course_teacher.uid)
    return sel2

@pytest.fixture
def course_students():
    students = [
        Users(uid="student_sel2_" + str(i), is_teacher=False, is_admin=False)
            for i in range(5)
    ]
    return students

@pytest.fixture
def course_students_relation(course,course_students):
    course_relations = [
        CourseStudents(course_id=course.course_id, uid=course_students[i].uid)
            for i in range(5)
    ]
    return course_relations

@pytest.fixture
def assistent():
    assist = Users(uid="assistent_sel2")
    return assist

@pytest.fixture()
def course_admin(course,assistent):
    admin_relation = CourseAdmins(uid=assistent.uid, course_id=course.course_id)
    return admin_relation

@pytest.fixture()
def valid_project(course):
    deadline = datetime(2024, 2, 25, 12, 0, 0)  # February 25, 2024, 12:00 PM
    project = Projects(
        title="Project",
        descriptions="Test project",
        deadline=deadline,
        course_id=course.course_id,
        visible_for_students=True,
        archieved=False,
    )
    return project
