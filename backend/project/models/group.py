"""Group model"""
from dataclasses import dataclass
from sqlalchemy import Integer, Column, ForeignKey
from project import db

@dataclass
class Group(db.Model):
    """
    This class will contain the model for the groups
    """
    __tablename__ = "groups"

    group_id: int = Column(Integer, primary_key=True)
    project_id: int = Column(Integer, ForeignKey("projects.project_id"), nullable=False, ondelete="CASCADE", primary_key=True)
    group_size: int = Column(Integer, nullable=False)
