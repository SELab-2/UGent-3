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
# mss https://graph.microsoft.com/oidc/userinfo


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
        response = requests.get(AUTHENTICATION_URL, headers=auth_header)
        if response.status_code != 200:
            abort(401) # TODO error message meegeven van request

        user_info = response.json()
        kwargs["AuthenticatedUserID"] = user_info["id"] # of enkel id van de user die request maakt toevoegen?
        try:
            user = db.session.get(User, user_info["id"])
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500

        if user:
            return f(*args, **kwargs)
        is_teacher = False
        if user_info["jobTitle"] != None:
            is_teacher = True
        # toevoegen
        try:
            new_user = User(uid=user_info["id"], is_teacher=is_teacher, is_admin=False)
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError:
                # every exception should result in a rollback
                db.session.rollback()
                return {"message": "An error occurred while creating the user",
                        "url": f"{API_URL}/users"}, 500
        return f(*args, **kwargs)
    return wrap


def authorize_teacher(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]:
            abort(500)
        

        # abort(403)
        return f(*args, **kwargs)
    return wrap


def authorize_teacher_of_course(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]:
            abort(500)
        


        # abort(403)
        return f(*args, **kwargs)
    return wrap


def authorize_teacher_or_course_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]:
            abort(500)
        #abort(403)
        return f(*args, **kwargs)
    return wrap


def authorize_student_of_course(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]:
            abort(500)
        
        return f(*args, **kwargs)
    return wrap