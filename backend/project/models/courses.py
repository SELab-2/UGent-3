"""The Course model"""

from sqlalchemy import Integer, Column, ForeignKey, String
from project import db

class Course(db.Model):
    """This class described the courses table, 
    a course has an id, name, optional ufora id and the teacher that created it"""

    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    ufora_id = Column(String(50), nullable=True)
    teacher = Column(String(255), ForeignKey("users.uid"), nullable=False)
