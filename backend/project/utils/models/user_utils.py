"""This module contains helper functions related to users for accessing the database"""

from os import getenv

from dotenv import load_dotenv

from flask import abort, make_response
from sqlalchemy.exc import SQLAlchemyError

from project import db
from project.models.user import User, Role

load_dotenv()
API_URL = getenv("API_HOST")

def get_user(user_id):
    """Returns the user associated with user_id or the appropriate error"""
    try:
        user = db.session.get(User, user_id)
    except SQLAlchemyError:
        db.session.rollback()
        abort(make_response(({"message": "An error occurred while fetching the user"}
                            , 500)))
    if not user:
        abort(make_response(({"message":f"User with id: {user_id} not found"}, 404)))
    return user

def is_teacher(auth_user_id):
    """This function checks whether the user with auth_user_id is a teacher"""
    user = get_user(auth_user_id)
    return user.role == Role.TEACHER

def is_admin(auth_user_id):
    """This function checks whether the user with auth_user_id is a teacher"""
    user = get_user(auth_user_id)
    return user.role == Role.ADMIN
