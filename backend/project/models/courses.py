"""The Courses model"""
# pylint: disable=too-few-public-methods
from sqlalchemy import INTEGER, Column, ForeignKey, String
from project import db


class Courses(db.Model):
    """Course model"""

    __tablename__ = "courses"
    course_id = Column(INTEGER, primary_key=True)
    name = Column(String(50), nullable=False)
    ufora_id = Column(String(50), nullable=True)
    teacher = Column(String(255), ForeignKey("Users.uid"), nullable=False)
