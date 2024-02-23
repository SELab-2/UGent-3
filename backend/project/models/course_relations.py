"""Models for relation between users and courses"""
# pylint: disable=too-few-public-methods

from sqlalchemy import Integer, Column, ForeignKey, PrimaryKeyConstraint, String
from project import db

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

class CourseAdmins(BaseCourseRelation):
    """Admin to course relation model"""

    __tablename__ = "course_admins"

class CourseStudents(BaseCourseRelation):
    """Student to course relation model"""

    __tablename__ = "course_students"
