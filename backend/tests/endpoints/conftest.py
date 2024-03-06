""" Configuration for pytest, Flask, and the test client."""

import os
from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project import create_app_with_db
from project.db_in import url, db
from project.models.users import User
from project.models.courses import Course
from project.models.course_relations import CourseAdmin
from project.models.course_relations import CourseStudent
from project.models.projects import Project
from project.models.submissions import Submission

@pytest.fixture
def users():
    """Return a list of users to populate the database"""
    return [
        User(uid="brinkmann", is_admin=True, is_teacher=True),
        User(uid="laermans", is_admin=True, is_teacher=True),
        User(uid="student01", is_admin=False, is_teacher=False),
        User(uid="student02", is_admin=False, is_teacher=False)
    ]

@pytest.fixture
def courses():
    """Return a list of courses to populate the database"""
    return [
        Course(name="AD3", teacher="brinkmann"),
        Course(name="RAF", teacher="laermans"),
    ]

@pytest.fixture
def course_relations(courses):
    """Returns a list of course relations to populate the database"""
    course_id_ad3 = courses[0].course_id
    course_id_raf = courses[1].course_id

    return [
        CourseAdmin(course_id=course_id_ad3, uid="brinkmann"),
        CourseStudent(course_id=course_id_ad3, uid="student01"),
        CourseStudent(course_id=course_id_ad3, uid="student02"),
        CourseAdmin(course_id=course_id_raf, uid="laermans"),
        CourseStudent(course_id=course_id_raf, uid="student02")
    ]

@pytest.fixture
def projects(courses):
    """Return  a list of projects to populate the database"""
    course_id_ad3 = courses[0].course_id
    course_id_raf = courses[1].course_id

    return [
        Project(
            title="B+ Trees",
            descriptions="Implement B+ trees",
            assignment_file="assignement.pdf",
            deadline=datetime(2024,3,15,13,0,0),
            course_id=course_id_ad3,
            visible_for_students=True,
            archieved=False,
            test_path="/tests",
            script_name="script.sh",
            regex_expressions=["*"]
        ),
        Project(
            title="Predicaten",
            descriptions="Predicaten project",
            assignment_file="assignment.pdf",
            deadline=datetime(2023,3,15,13,0,0),
            course_id=course_id_raf,
            visible_for_students=False,
            archieved=True,
            test_path="/tests",
            script_name="script.sh",
            regex_expressions=["*"]
        )
    ]

@pytest.fixture
def submissions(projects):
    """Return a list of submissions to populate the database"""
    project_id_ad3 = projects[0].project_id
    project_id_raf = projects[1].project_id

    return [
        Submission(
            uid="student01",
            project_id=project_id_ad3,
            grading=16,
            submission_time=datetime(2024,3,14,12,0,0),
            submission_path="/submissions/1",
            submission_status=True
        ),
        Submission(
            uid="student02",
            project_id=project_id_ad3,
            submission_time=datetime(2024,3,14,23,59,59),
            submission_path="/submissions/2",
            submission_status=False
        ),
        Submission(
            uid="student02",
            project_id=project_id_raf,
            grading=15,
            submission_time=datetime(2023,3,5,10,0,0),
            submission_path="/submissions/3",
            submission_status=True
        )
    ]

engine = create_engine(url)
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
