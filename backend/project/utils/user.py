"""Utility functions for the user model"""

from typing import Tuple
from sqlalchemy.orm import Session
from project.models.user import User

def is_valid_user(session: Session, uid: any) -> Tuple[bool, str]:
    """Check if a uid is valid

    Args:
        session (Session): A database session
        uid (any): The uid

    Returns:
        Tuple[bool, str]: Is valid
    """
    if uid is None:
        return False, "The uid is missing"

    if not isinstance(uid, str):
        return False, f"Invalid uid typing (uid={uid})"

    user = session.get(User, uid)
    if user is None:
        return False, f"Invalid user (uid={uid})"
    return True, "Valid user"
