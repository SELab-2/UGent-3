"""Project model"""

from dataclasses import dataclass
from enum import Enum
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Enum as EnumField)

from sqlalchemy_utils import CompositeType
from project.db_in import db

class Runner(str, Enum):
    """Enum for Runner"""
    PYTHON = 'PYTHON'
    GENERAL = 'GENERAL'
    CUSTOM = 'CUSTOM'

@dataclass
class Project(db.Model): # pylint: disable=too-many-instance-attributes
    """This class describes the projects table,
    a projects has an id, a title, a description, 
    an optional assignment file that can contain more explanation of the projects,
    an optional deadline,
    the course id of the course to which the project belongs,
    visible for students variable so a teacher can decide if the students can see it yet,
    archived var so we can implement the archiving functionality,
    a test path,script name and regex expressions for automated testing

    Pylint disable too many instance attributes because we can't reduce the amount
     of fields of the model
    """

    __tablename__ = "projects"
    project_id: int = Column(Integer, primary_key=True)
    title: str = Column(String(50), nullable=False, unique=False)
    description: str = Column(Text, nullable=False)
    deadlines: list = Column(ARRAY(
        CompositeType(
            "deadline",
            [
                Column("description", Text),
                Column("deadline", DateTime(timezone=True))
            ]
            ),
        dimensions=1
        )
    )
    course_id: int = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    visible_for_students: bool = Column(Boolean, nullable=False)
    archived: bool = Column(Boolean, nullable=False)
    groups_locked: bool = Column(Boolean)
    runner: Runner = Column(
        EnumField(Runner, name="runner"),
        nullable=False)
    regex_expressions: list[str] = Column(ARRAY(String(50)))
