"""Model for relation between groups and students"""
from dataclasses import dataclass
from sqlalchemy import Integer, Column, ForeignKey
from project.db_in import db

@dataclass
class GroupStudent(db.Model):
    """Model for relation between groups and students"""
    __tablename__ = "group_students"

    group_id: int = Column(Integer, ForeignKey("groups.group_id"), primary_key=True)
    uid: str = Column(Integer, ForeignKey("users.uid"), primary_key=True)
