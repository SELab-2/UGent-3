"""
Course Share Code Model
"""


from dataclasses import dataclass
import uuid
from sqlalchemy import Integer, Column, ForeignKey, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from project import db

@dataclass
class CourseShareCode(db.Model):
    """
    This class will contain the model for the course share codes
    """
    __tablename__ = "course_join_codes"

    join_code: int = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id: int = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    expiry_time: str = Column(Date, nullable=True)
    for_admins: bool = Column(Boolean, nullable=False)
