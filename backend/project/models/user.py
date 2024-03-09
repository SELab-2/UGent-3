"""Model for users"""
import dataclasses

from sqlalchemy import Boolean, Column, String
from project import db

@dataclasses.dataclass
class User(db.Model):
    """This class defines the users table,
    a user has a uid,
    is_teacher and is_admin booleans because a user 
    can be either a student,admin or teacher"""

    __tablename__ = "users"
    uid:str = Column(String(255), primary_key=True)
    is_teacher:bool = Column(Boolean)
    is_admin:bool = Column(Boolean)
