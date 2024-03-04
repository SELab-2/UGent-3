"""Model for projects"""
from sqlalchemy import ARRAY, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from project import db

class Project(db.Model):
    """This class describes the projects table,
    a projects has an id, a title, a description, 
    an optional assignment file that can contain more explanation of the projects,
    an optional deadline,
    the course id of the course to which the project belongs,
    visible for students variable so a teacher can decide if the students can see it yet,
    archieved var so we can implement the archiving functionality,
    a test path,script name and regex experssions for automated testing"""

    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, unique=False)
    descriptions = Column(Text, nullable=False)
    assignment_file = Column(String(50))
    deadline = Column(DateTime(timezone=True))
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    visible_for_students = Column(Boolean, nullable=False)
    archieved = Column(Boolean, nullable=False)
    test_path = Column(String(50))
    script_name = Column(String(50))
    regex_expressions = Column(ARRAY(String(50)))
