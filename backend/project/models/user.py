"""User model"""

from enum import Enum
from dataclasses import dataclass
from sqlalchemy import Column, String, Enum as EnumField
from project.db_in import db

class Role(Enum):
    """This class defines the roles of a user"""
    STUDENT = 0
    TEACHER = 1
    ADMIN = 2

@dataclass
class User(db.Model):
    """
    This class defines the users table
    a user has a uid,
    a display_name and a role, 
    this role can be either student, admin or teacher
    """

    __tablename__ = "users"
    uid: str = Column(String(255), primary_key=True)
    display_name: str = Column(String(255))
    role: Role = Column(EnumField(Role), nullable=False)
    def to_dict(self):
        """
        Converts a User to a serializable dict
        """
        return {
            'uid': self.uid,
            'role': self.role.name,  # Convert the enum to a string
            'display_name': self.display_name
        }
