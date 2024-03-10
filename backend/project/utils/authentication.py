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
from project.models.courses import Course
from project.models.projects import Project
from project.models.course_relations import CourseAdmin, CourseStudent
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()
API_URL = getenv("API_HOST")
AUTHENTICATION_URL = "https://graph.microsoft.com/v1.0/me"
# maybe https://graph.microsoft.com/oidc/userinfo -> this returns less data


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
        kwargs["AuthenticatedUserID"] = user_info["id"]
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
        # add user if not yet in database
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
        # finding the user in the db should theoretically not be necessary but is an extra safety check, because it means the user was
        # correctly authenticated beforehand
        if not kwargs["AuthenticatedUserID"]: # should realistically never happen
            abort(500)
        try:
            user = db.session.get(User, kwargs["AuthenticatedUserID"])
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500
        if not user: # should realistically never happen
            abort(500)
        if user.is_teacher:
            return f(*args, **kwargs)
        abort(403)
    return wrap


def authorize_teacher_of_course(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]: # should realistically never happen
            abort(500)
        try:
            user = db.session.get(User, kwargs["AuthenticatedUserID"])
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500
        if not user: # should realistically never happen
            abort(500)

        # find teacher of course
        course_id = request.args["course_id"] # TODO check if this is how you get course_id from url
        if not course_id:
            abort(500)
        
        try:
            course = db.session.get(Course, course_id)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500

        if not course:
            abort(500)

        if kwargs["AuthenticatedUserID"] == course.teacher:
            return f(*args, **kwargs)

        abort(403)
    return wrap


def authorize_teacher_or_course_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]: # should realistically never happen
            abort(500)
        try:
            user = db.session.get(User, kwargs["AuthenticatedUserID"])
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500
        if not user: # should realistically never happen
            abort(500)

        # find teacher of course
        course_id = request.args["course_id"]
        if not course_id:
            abort(500)
        
        try:
            course = db.session.get(Course, course_id)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500

        if not course:
            abort(500)

        if kwargs["AuthenticatedUserID"] == course.teacher:
            return f(*args, **kwargs)

        try:
            course_admin = db.session.get(CourseAdmin, course_id + user.uid) # TODO check if this is correct primary key
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500

        if course_admin:
            return f(*args, **kwargs)

        abort(403)
    return wrap


def authorize_student_of_course(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]: # should realistically never happen
            abort(500)
        try:
            user = db.session.get(User, kwargs["AuthenticatedUserID"])
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500
        if not user: # should realistically never happen
            abort(500)

        # find course
        course_id = request.args["course_id"]
        if not course_id:
            abort(500)
        
        try:
            course = db.session.get(Course, course_id)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500

        if not course:
            abort(500)
        
        try:
            course_student = db.session.get(CourseStudent, course_id + user.uid) # TODO check if this is correct primary key
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500

        if course_student:
            return f(*args, **kwargs)

        abort(403)
    return wrap


def authorize_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]: # should realistically never happen
            abort(500)
        try:
            user = db.session.get(User, kwargs["AuthenticatedUserID"])
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500
        if not user: # should realistically never happen
            abort(500)

        
        user_id = request.args["user_id"]

        if user.uid == user_id:
            return f(*args, **kwargs)
        
        abort(403)
    return wrap


def authorize_teacher_of_project(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]: # should realistically never happen
            abort(500)
        try:
            user = db.session.get(User, kwargs["AuthenticatedUserID"])
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500
        if not user: # should realistically never happen
            abort(500)

        project_id = request.args["project_id"]

        try:
            project = db.session.get(Project, project_id)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the project",
                        "url": f"{API_URL}/users"}, 500

        if not project:
            abort(404)

        # find teacher of course
        course_id = project.course_id # TODO check if this is how you get course_id from url
        if not course_id:
            abort(500)
        
        try:
            course = db.session.get(Course, course_id)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the course",
                        "url": f"{API_URL}/users"}, 500

        if not course:
            abort(500)

        if kwargs["AuthenticatedUserID"] == course.teacher:
            return f(*args, **kwargs)

        abort(403)
    return wrap


def authorize_teacher_or_project_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]: # should realistically never happen
            abort(500)
        try:
            user = db.session.get(User, kwargs["AuthenticatedUserID"])
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500
        if not user: # should realistically never happen
            abort(500)

        project_id = request.args["project_id"]

        try:
            project = db.session.get(Project, project_id)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the project",
                        "url": f"{API_URL}/users"}, 500

        if not project:
            abort(500)

        # find teacher of course
        course_id = project.course_id # TODO check if this is how you get course_id from url
        if not course_id:
            abort(500)
        
        try:
            course = db.session.get(Course, course_id)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the course",
                        "url": f"{API_URL}/users"}, 500

        if not course:
            abort(500)

        if kwargs["AuthenticatedUserID"] == course.teacher:
            return f(*args, **kwargs)
        
        try:
            course_admin = db.session.get(CourseAdmin, course_id + user.uid) # TODO check if this is correct primary key
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500

        if course_admin:
            return f(*args, **kwargs)

        abort(403)
    return wrap


def authorize_project_visible(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not kwargs["AuthenticatedUserID"]: # should realistically never happen
            abort(500)
        try:
            user = db.session.get(User, kwargs["AuthenticatedUserID"])
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500
        if not user: # should realistically never happen
            abort(500)
        
        project_id = request.args["project_id"]

        try:
            project = db.session.get(Project, project_id)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the project",
                        "url": f"{API_URL}/users"}, 500

        if not project:
            abort(500)

        # find teacher of course
        course_id = project.course_id # TODO check if this is how you get course_id from url
        if not course_id:
            abort(500)
        
        try:
            course = db.session.get(Course, course_id)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the course",
                        "url": f"{API_URL}/users"}, 500

        if not course:
            abort(500)

        if kwargs["AuthenticatedUserID"] == course.teacher:
            return f(*args, **kwargs)
        
        try:
            course_admin = db.session.get(CourseAdmin, course_id + user.uid) # TODO check if this is correct primary key
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500

        if course_admin:
            return f(*args, **kwargs)

        try:
            course_student = db.session.get(CourseStudent, course_id + user.uid) # TODO check if this is correct primary key
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500
        
        if course_student:
            if project.visible_for_students:
                return f(*args, **kwargs)
        abort(403)   
    return wrap