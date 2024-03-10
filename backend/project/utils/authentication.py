"""
This module contains the functions to authenticate API calls.
"""
from os import getenv

from dotenv import load_dotenv

from functools import wraps
from flask import abort, request
import requests

from project import db

from project.models.users import User
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()
API_URL = getenv("API_HOST")
AUTHENTICATION_URL = "https://graph.microsoft.com/v1.0/me"


def login_required(f):
    """
    This function will check if the person sending a request to the API is logged in
    and additionally create their user entry in the database if necessary
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        authentication = request.headers.get("Authorization")
        if not authentication:
            abort(401)
        auth_header = {"Authorization": authentication}
        user_info = requests.get(AUTHENTICATION_URL, headers=auth_header).json()
        # hier nog controleren of user wel juiste access token had
        
        # header toevoegen in request voor volgende decorator?
        request.headers.add_header("AuthenticatedUserID", ) # of enkel id van de user die request maakt toevoegen?
        try:
            user = db.session.get(User, uid)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500

        if user:
            return f(*args, **kwargs)
        
        # toevoegen
        try:
            new_user = User(uid=uid, is_teacher=is_teacher, is_admin=False)
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError:
                # every exception should result in a rollback
                db.session.rollback()
                return {"message": "An error occurred while creating the user",
                        "url": f"{API_URL}/users"}, 500
        return f(*args, **kwargs)
    return wrap


def authenticate_teacher(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        
        return 0
    return wrap


def authenticate_teacher_or_course_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        
        return 0
    return wrap
