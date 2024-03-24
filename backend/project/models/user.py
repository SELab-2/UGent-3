"""User model"""

from dataclasses import dataclass
from sqlalchemy import Boolean, Column, String
from project.db_in import db

@dataclass
class User(db.Model):
    """This class defines the users table,
    a user has a uid, 
    a display_name,
    is_teacher and is_admin booleans because a user 
    can be either a student, admin or teacher"""

    __tablename__ = "users"
    uid: str = Column(String(255), primary_key=True)
    display_name: str = Column(String(255))
    is_teacher: bool = Column(Boolean)
    is_admin: bool = Column(Boolean)
