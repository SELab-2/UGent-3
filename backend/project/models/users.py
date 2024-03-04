"""Model for users"""
from sqlalchemy import Boolean, Column, String
from project import db


class Users(db.Model):
    """This class defines the users table,
    a user has an uid,
    is_teacher and is_admin booleans because a user 
    can be either a student,admin or teacher"""

    __tablename__ = "users"
    uid = Column(String(255), primary_key=True)
    is_teacher = Column(Boolean)
    is_admin = Column(Boolean)
