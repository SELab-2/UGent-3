"""Model for users"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Boolean, Column, String
from project import db


class Users(db.Model):
    """User model"""

    __tablename__ = "users"
    uid = Column(String(255), primary_key=True)
    is_teacher = Column(Boolean)
    is_admin = Column(Boolean)
