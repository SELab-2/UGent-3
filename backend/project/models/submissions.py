"""Model for submissions"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column,String,ForeignKey,Integer,CheckConstraint,DateTime,Boolean
from project import db

class Submissions(db.Model):
    """Submission model"""

    __tablename__ = "submissions"
    submission_id = Column(Integer, nullable=False, primary_key=True)
    uid = Column(String(255), ForeignKey("Users.uid"), nullable=False)
    project_id = Column(Integer, ForeignKey("Projects.project_id"), nullable=False)
    grading = Column(Integer, CheckConstraint("grading >= 0 AND grading <= 20"))
    submission_time = Column(DateTime(timezone=True), nullable=False)
    submission_path = Column(String(50), nullable=False)
    submission_status = Column(Boolean, nullable=False)
