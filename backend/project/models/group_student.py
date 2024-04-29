"""Model for relation between groups and students"""
from dataclasses import dataclass
from sqlalchemy import Integer, Column, ForeignKey, String
from project.db_in import db

@dataclass
class GroupStudent(db.Model):
    """Model for relation between groups and students"""
    __tablename__ = "group_students"

    uid: str = Column(String(255), ForeignKey("users.uid"), primary_key=True)
    group_id: int = Column(Integer, ForeignKey("groups.group_id"), primary_key=True)
    project_id: int = Column(Integer, ForeignKey("groups.project_id"), primary_key=True)
