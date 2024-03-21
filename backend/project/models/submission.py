"""Submission model"""

from dataclasses import dataclass
from sqlalchemy import Column, String, ForeignKey, Integer, CheckConstraint, DateTime, Boolean, Float
from project.db_in import db

@dataclass
class Submission(db.Model):
    """This class describes the submissions table,
    submissions can be made to a project, a submission has
    and id, a uid from the user that uploaded it, 
    the project id of the related project,
    an optional grading,
    the submission time,
    submission path,
    and finally the submission status
    so we can easily present in a list which submission succeeded the automated checks"""

    __tablename__ = "submissions"
    submission_id: int = Column(Integer, primary_key=True)
    uid: str = Column(String(255), ForeignKey("users.uid"), nullable=False)
    project_id: int = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    grading: float = Column(Float, CheckConstraint("grading >= 0 AND grading <= 20"))
    submission_time: DateTime = Column(DateTime(timezone=True), nullable=False)
    submission_path: str = Column(String(50), nullable=False)
    submission_status: bool = Column(Boolean, nullable=False)
