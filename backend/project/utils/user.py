"""Utility functions for the user model"""

from typing import Tuple
from requests import Response

from flask import abort, make_response

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from project import db
from project.models.user import User, Role

def get_or_make_user(profile_res: Response) -> User:
    """
    Function to create a new User in the database or return
    the user associated with the profile_res received from authentication
    
    Returns either a database error or the User data.
    """
    auth_user_id = profile_res.json()["id"]
    try:
        user = db.session.get(User, auth_user_id)
    except SQLAlchemyError:
        db.session.rollback()
        abort(make_response(({"message":
                            "An unexpected database error occured while fetching the user"},
                            500)))

    if not user:
        role = Role.STUDENT
        if profile_res.json()["jobTitle"] is not None:
            role = Role.TEACHER

        # add user if not yet in database
        try:
            new_user = User(uid=auth_user_id,
                            role=role,
                            display_name=profile_res.json()["displayName"])
            db.session.add(new_user)
            db.session.commit()
            user = new_user
        except SQLAlchemyError:
            db.session.rollback()
            abort(make_response(({"message":
                                    """An unexpected database error occured
                                while creating the user during authentication"""}, 500)))
    return user

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
