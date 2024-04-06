"""Root level fixtures"""

from datetime import datetime
from zoneinfo import ZoneInfo
from pytest import fixture
from project.sessionmaker import engine, Session
from project.db_in import db
from project.models.course import Course
from project.models.user import User,Role
from project.models.project import Project
from project.models.course_relation import CourseStudent,CourseAdmin
from project.models.submission import Submission, SubmissionStatus

@fixture
def db_session():
    """Create a new database session for a test.
    After the test, all changes are rolled back and the session is closed."""

    db.metadata.create_all(engine)
    session = Session()

    try:
        yield session
    finally:
        # Rollback
        session.rollback()
        session.close()

        # Truncate all tables
        for table in reversed(db.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()

def users():
    """Return a list of users to populate the database"""
    return [
        User(uid="brinkmann", role=Role.ADMIN),
        User(uid="laermans", role=Role.ADMIN),
        User(uid="student01", role=Role.STUDENT),
        User(uid="student02", role=Role.STUDENT)
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
            deadlines=[("Deadline 1",datetime(2024,3,15,13,0,0))],
            course_id=course_id_ad3,
            visible_for_students=True,
            archived=False,
            regex_expressions=["solution"]
        ),
        Project(
            title="Predicaten",
            description="Predicaten project",
            deadlines=[("Deadline 1", datetime(2023,3,15,13,0,0))],
            course_id=course_id_raf,
            visible_for_students=False,
            archived=True,
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
            submission_status= SubmissionStatus.SUCCESS
        ),
        Submission(
            uid="student02",
            project_id=project_id_ad3,
            submission_time=datetime(2024,3,14,23,59,59,tzinfo=ZoneInfo("GMT")),
            submission_path="/submissions/2",
            submission_status= SubmissionStatus.FAIL
        ),
        Submission(
            uid="student02",
            project_id=project_id_raf,
            grading=15,
            submission_time=datetime(2023,3,5,10,0,0,tzinfo=ZoneInfo("GMT")),
            submission_path="/submissions/3",
            submission_status= SubmissionStatus.SUCCESS
        )
    ]

### AUTHENTICATION & AUTHORIZATION ###
def auth_tokens():
    """Add the authenticated users to the database"""

    return [
        User(uid="login", role=Role.STUDENT),
        User(uid="student", role=Role.STUDENT),
        User(uid="student_other", role=Role.STUDENT),
        User(uid="teacher", role=Role.TEACHER),
        User(uid="teacher_other", role=Role.TEACHER),
        User(uid="admin", role=Role.ADMIN),
        User(uid="admin_other", role=Role.ADMIN)
    ]

### SESSION ###
@fixture
def session():
    """Create a new database session for a test.
    After the test, all changes are rolled back and the session is closed."""

    db.metadata.create_all(engine)
    session = Session()

    try:
        session.add_all(auth_tokens())

        # Populate the database
        session.add_all(users())
        session.commit()
        session.add_all(courses())
        session.commit()
        session.add_all(course_relations(session))
        session.commit()
        session.add_all(projects(session))
        session.commit()
        session.add_all(submissions(session))
        session.commit()

        yield session
    finally:
        # Rollback
        session.rollback()
        session.close()

        # Truncate all tables
        for table in reversed(db.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
