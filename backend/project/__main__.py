"""Main entry point for the application."""
from sys import path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Column,
    PrimaryKeyConstraint,
    String,
    Boolean,
    Integer,
    Text,
)


path.append(".")

if __name__ == "__main__":
    from project import create_app

    app = create_app()
    app.run(debug=True)
    db = SQLAlchemy(app)  # Create db after app is created

    class Users(db.Model):
        """User model"""

        __tablename__ = "users"  # table name needs to match sql!
        uid = Column(String(255), primary_key=True)
        is_teacher = Column(Boolean)
        is_admin = Column(Boolean)

    class Courses(db.Model):
        """Course model"""

        __tablename__ = "courses"
        course_id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        ufora_id = Column(String(50), nullable=True)
        teacher = Column(String(255), ForeignKey("Users.uid"), nullable=False)

    class BaseCourseRelation(db.Model):
        """Base class for course relation models"""

        __abstract__ = True

        course_id = Column(Integer, ForeignKey("Courses.course_id"), nullable=False)
        uid = Column(String(255), ForeignKey("Users.uid"), nullable=False)
        __table_args__ = (PrimaryKeyConstraint("course_id", "uid"),)

    class CourseAdmins(BaseCourseRelation):
        """Admin to course relation model"""

        __tablename__ = "course_admins"

    class CourseStudents(BaseCourseRelation):
        """Student to course relation model"""

        __tablename__ = "course_students"

    class Projects(db.Model):
        """Project model"""

        __tablename__ = "projects"
        project_id = Column(Integer, primary_key=True)
        title = Column(String(50), nullable=False, unique=False)
        descriptions = Column(Text, nullable=False)
        assignment_file = Column(String(50))
        deadline = Column(DateTime(timezone=True))
        course_id = Column(Integer, ForeignKey("Courses.course_id"), nullable=False)
        visible_for_students = Column(Boolean, nullable=False)
        archieved = Column(Boolean, nullable=False)
        test_path = Column(String(50))
        script_name = Column(String(50))
        regex_expressions = Column(ARRAY(String(50)))

    class Submissions(db.Model):
        """Submission model"""

        __tablename__ = "submissions"
        submission_id = Column(Integer, nullable=False, primary_key=True)
        uid = Column(String(255), ForeignKey("Users.uid"), nullable=False)
        project_id = Column(Integer, ForeignKey("Projects.project_id"), nullable=False)
        grading = Column(Integer, CheckConstraint("grading >= 0 AND grading <= 20"))
        submission_time = Column(DateTime(timezone=True), nullable=False)
        submission_path = Column(String(50), nullable=False)
        submission_status = Column(Boolean, nullable=False)
