"""Model for submissions"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column,String,ForeignKey,Integer,CheckConstraint,DateTime,Boolean
from project import db
from project.models.users import Users

class Submissions(db.Model):
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
    submission_id = Column(Integer, nullable=False, primary_key=True)
    uid = Column(String(255), ForeignKey("users.uid"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    grading = Column(Integer, CheckConstraint("grading >= 0 AND grading <= 20"))
    submission_time = Column(DateTime(timezone=True), nullable=False)
    submission_path = Column(String(50), nullable=False)
    submission_status = Column(Boolean, nullable=False)
