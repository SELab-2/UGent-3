"""Model for projects"""
# pylint: disable=too-few-public-methods
from sqlalchemy import ARRAY, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from project import db

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
