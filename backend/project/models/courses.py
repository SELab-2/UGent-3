from sqlalchemy import Integer, Column, ForeignKey, String
from project import db
from dataclasses import dataclass

"""The Course model"""


@dataclass
class Course(db.Model):
    """This class described the courses table, 
    a course has an id, name, optional ufora id and the teacher that created it"""

    __tablename__: str = "courses"
    course_id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False)
    ufora_id: str = Column(String(50), nullable=True)
    teacher: str = Column(String(255), ForeignKey("users.uid"), nullable=False)
