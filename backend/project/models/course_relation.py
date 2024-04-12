"""Course relation model"""

from dataclasses import dataclass
from sqlalchemy import Integer, Column, ForeignKey, String
from project.db_in import db

@dataclass
class BaseCourseRelation(db.Model):
    """Base class for course relation models,
    both course relation tables have a 
    course_id of the course to wich someone is related and
    an uid of the related person"""

    __abstract__ = True

    course_id: int = Column(Integer, ForeignKey('courses.course_id'), primary_key=True)
    uid: str = Column(String(255), ForeignKey("users.uid"), primary_key=True)

class CourseAdmin(BaseCourseRelation):
    """Admin to course relation model"""

    __tablename__ = "course_admins"

class CourseStudent(BaseCourseRelation):
    """Student to course relation model"""

    __tablename__ = "course_students"
