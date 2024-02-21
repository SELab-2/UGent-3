"""Models for relation between users and courses"""
# pylint: disable=too-few-public-methods

from sqlalchemy import Integer, Column, ForeignKey, PrimaryKeyConstraint, String
from project import db

class BaseCourseRelation(db.Model):
    """Base class for course relation models"""

    __abstract__ = True

    course_id = Column(Integer, ForeignKey('Courses.course_id'), nullable=False)
    uid = Column(String(255), ForeignKey("Users.uid"), nullable=False)
    __table_args__ = PrimaryKeyConstraint("course_id", "uid")

class CourseAdmins(BaseCourseRelation):
    """Admin to course relation model"""

    __tablename__ = "course_admins"

class CourseStudents(BaseCourseRelation):
    """Student to course relation model"""

    __tablename__ = "course_students"
