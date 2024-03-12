"""
This module contains the functions to authenticate API calls.
"""
from os import getenv

from dotenv import load_dotenv

from functools import wraps
from flask import abort, request, make_response
import requests

from project import db

from project.models.users import User
from project.models.courses import Course
from project.models.projects import Project
from project.models.course_relations import CourseAdmin, CourseStudent
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()
API_URL = getenv("API_HOST")
AUTHENTICATION_URL = getenv("AUTHENTICATION_URL")
# maybe https://graph.microsoft.com/oidc/userinfo -> this returns less data


def abort_with_message(code: int, message: str):
    abort(make_response({"message": message}, code))


def not_allowed(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        abort_with_message(403, "You are not authorized to perfom this action")
    return wrap


def return_authenticated_user_id():
    authentication = request.headers.get("Authorization")
    if not authentication:
        abort_with_message(401, "No authorization given, you need an access token to use this API")
        
    auth_header = {"Authorization": authentication}
    response = requests.get(AUTHENTICATION_URL, headers=auth_header)
    if response.status_code != 200:
          abort_with_message(401, response.json()["error"])

    user_info = response.json()
    auth_user_id = user_info["id"]
    try:
        user = db.session.get(User, auth_user_id)
    except SQLAlchemyError:
        # every exception should result in a rollback
        db.session.rollback()
        return abort_with_message(500, "An unexpected database error occured while fetching the user")
    
    if user:
        return auth_user_id
    is_teacher = False
    if user_info["jobTitle"] != None: # TODO check what this is for an actual teacher
        is_teacher = True
    
    # add user if not yet in database
    try:
        new_user = User(uid=auth_user_id, is_teacher=is_teacher, is_admin=False)
        db.session.add(new_user)
        db.session.commit()
    except SQLAlchemyError:
            # every exception should result in a rollback
            db.session.rollback()
            return abort_with_message(500, "An unexpected database error occured while creating the user")
    return auth_user_id
    

def is_teacher(auth_user_id):
    try:
        user = db.session.get(User, auth_user_id)
    except SQLAlchemyError:
        # every exception should result in a rollback
        db.session.rollback()
        return {"message": "An error occurred while fetching the user",
                        "url": f"{API_URL}/users"}, 500
    if not user: # should realistically never happen
            abort(500)
    if user.is_teacher:
        return True
    return False


def is_teacher_of_course(auth_user_id, course_id):
    try:
        course = db.session.get(Course, course_id)
    except SQLAlchemyError:
    # every exception should result in a rollback
        db.session.rollback()
        return {"message": "An error occurred while fetching the user",
                    "url": f"{API_URL}/users"}, 500

    if not course:
        abort(404)

    if auth_user_id == course.teacher:
        return True


def is_admin_of_course(auth_user_id, course_id):
    try:
        course_admin = db.session.get(CourseAdmin, course_id + auth_user_id) # TODO check if this is correct primary key
    except SQLAlchemyError:
    # every exception should result in a rollback
        db.session.rollback()
        return {"message": "An error occurred while fetching the user",
                    "url": f"{API_URL}/users"}, 500

    if course_admin:
        return True

    return False


def is_student_of_course(auth_user_id, course_id):
    try:
        course_student = db.session.get(CourseStudent, course_id + auth_user_id) # TODO check if this is correct primary key
    except SQLAlchemyError:
        # every exception should result in a rollback
        db.session.rollback()
        return {"message": "An error occurred while fetching the user",
                    "url": f"{API_URL}/users"}, 500
    if course_student:
        return True
    return False


def get_course_of_project(project_id):
    try:
        project = db.session.get(Project, project_id)
    except SQLAlchemyError:
    # every exception should result in a rollback
        db.session.rollback()
        return {"message": "An error occurred while fetching the project",
                    "url": f"{API_URL}/users"}, 500

    if not project:
        abort(404)

    return project.course_id


def login_required(f):
    """
    This function will check if the person sending a request to the API is logged in
    and additionally create their user entry in the database if necessary
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        return_authenticated_user_id()
        return f(*args, **kwargs)
    return wrap


def authorize_teacher(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        if is_teacher(auth_user_id):
            return f(*args, **kwargs)
        abort_with_message(403, "You are not authorized to perfom this action, only teachers are authorized")
    return wrap


def authorize_teacher_of_course(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        if is_teacher_of_course(auth_user_id, request.args["course_id"]):
            return f(*args, **kwargs)

        abort_with_message(403)
    return wrap


def authorize_teacher_or_course_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        course_id = request.args["course_id"]
        if is_teacher_of_course(auth_user_id, course_id) or is_admin_of_course(auth_user_id, course_id):
            return f(*args, **kwargs)

        abort_with_message(403, "You are not authorized to perfom this action, only teachers and course admins are authorized")
    return wrap


def authorize_student_of_course(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        course_id = request.args["course_id"]
        if is_student_of_course(auth_user_id, course_id):
            return f(*args, **kwargs)
        abort_with_message(403, "You are not authorized to perfom this action, you are not a student of this course")
    return wrap


def authorize_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        user_id = request.args["user_id"]

        if auth_user_id == user_id:
            return f(*args, **kwargs)
        
        abort_with_message(403, "You are not authorized to perfom this action, you are not this user")
    return wrap


def authorize_teacher_of_project(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        project_id = request.args["project_id"]
        course_id = get_course_of_project(project_id)
        
        if is_teacher(auth_user_id, course_id):
            return f(*args, **kwargs)

        abort_with_message(403, "You are not authorized to perfom this action, you are not the teacher of this project")
    return wrap


def authorize_teacher_or_project_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        project_id = request.args["project_id"]
        course_id = get_course_of_project(project_id)
        if is_teacher_of_course(auth_user_id, course_id) or is_admin_of_course(auth_user_id, course_id):
            return f(*args, **kwargs)
        abort_with_message(403, """You are not authorized to perfom this action, 
                           you are not the teacher or an admin of this project""")
    return wrap


def authorize_project_visible(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        project_id = request.args["project_id"]
        course_id = get_course_of_project(project_id)
        if is_teacher_of_course(auth_user_id, course_id) or is_admin_of_course(auth_user_id, course_id):
            return f(*args, **kwargs)
        
        try:
            project = db.session.get(Project, project_id)
        except SQLAlchemyError:
        # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while fetching the project",
                    "url": f"{API_URL}/users"}, 500
        if not project:
            abort_with_message(404, "Project with given id not found")
        if is_student_of_course(auth_user_id, course_id) and project.visible_for_students:
            return f(*args, **kwargs)
        abort_with_message(403, "What project?")
    return wrap
