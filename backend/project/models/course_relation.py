"""Models for relation between users and courses"""
from sqlalchemy import Integer, Column, ForeignKey, PrimaryKeyConstraint, String
from project.db_in import db

class BaseCourseRelation(db.Model):
    """Base class for course relation models,
    both course relation tables have a 
    course_id of the course to wich someone is related and
    an uid of the related person"""

    __abstract__ = True

    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    uid = Column(String(255), ForeignKey("users.uid"), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("course_id", "uid"),
    )

class CourseAdmin(BaseCourseRelation):
    """Admin to course relation model"""

    __tablename__ = "course_admins"

class CourseStudent(BaseCourseRelation):
    """Student to course relation model"""

    __tablename__ = "course_students"
