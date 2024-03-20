"""
This module contains the functions to authenticate API calls.
"""
from os import getenv

from functools import wraps

from dotenv import load_dotenv

from flask import abort, request, make_response
import requests
from sqlalchemy.exc import SQLAlchemyError

from project import db

from project.models.user import User
from project.models.course import Course
from project.models.project import Project
from project.models.submission import Submission
from project.models.course_relation import CourseAdmin, CourseStudent
from project.utils.models import get_course, get_project, \
    get_submission, get_user

load_dotenv()
API_URL = getenv("API_HOST")
AUTHENTICATION_URL = getenv("AUTHENTICATION_URL")


def not_allowed(f):
    """Decorator function to immediately abort the current request and return 403: Forbidden"""
    @wraps(f)
    def wrap(*args, **kwargs):
        return {"message":"Forbidden action"}, 403
    return wrap


def return_authenticated_user_id():
    """This function will authenticate the request and check whether the authenticated user
    is already in the database, if not, they will be added
    """
    authentication = request.headers.get("Authorization")
    if not authentication:
        abort(make_response(({"message":
                              "No authorization given, you need an access token to use this API"}
                             , 401)))

    auth_header = {"Authorization": authentication}
    try:
        response = requests.get(AUTHENTICATION_URL, headers=auth_header, timeout=5)
    except TimeoutError:
        abort(make_response(({"message":"Request to Microsoft timed out"}
                             , 500)))
    if not response or response.status_code != 200:
        abort(make_response(({"message":
                              "An error occured while trying to authenticate your access token"}
                             , 401)))

    user_info = response.json()
    auth_user_id = user_info["id"]
    try:
        user = db.session.get(User, auth_user_id)
    except SQLAlchemyError:
        db.session.rollback()
        abort(make_response(({"message":
                "An unexpected database error occured while fetching the user"}, 500)))

    if user:
        return auth_user_id
    is_teacher = False
    if user_info["jobTitle"] is not None:
        is_teacher = True

    # add user if not yet in database
    try:
        new_user = User(uid=auth_user_id, is_teacher=is_teacher, is_admin=False)
        db.session.add(new_user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        abort(make_response(({"message":
                        """An unexpected database error occured 
                        while creating the user during authentication"""}, 500)))
    return auth_user_id

def is_teacher(auth_user_id):
    """This function checks whether the user with auth_user_id is a teacher"""
    user = get_user(auth_user_id)
    return user.is_teacher


def is_admin(auth_user_id):
    """This function checks whether the user with auth_user_id is a teacher"""
    user = get_user(auth_user_id)
    return user.is_admin


def is_teacher_of_course(auth_user_id, course_id):
    """This function checks whether the user 
    with auth_user_id is the teacher of the course: course_id
    """
    course = get_course(course_id)
    if auth_user_id == course.teacher:
        return True
    return False


def is_admin_of_course(auth_user_id, course_id):
    """This function checks whether the user 
    with auth_user_id is an admin of the course: course_id
    """
    try:
        course_admin = db.session.get(CourseAdmin, (course_id, auth_user_id))
    except SQLAlchemyError:
    # every exception should result in a rollback
        db.session.rollback()
        abort(make_response(({"message": "An error occurred while fetching the user",
                    "url": f"{API_URL}/users"}, 500)))

    if course_admin:
        return True
    return False


def is_student_of_course(auth_user_id, course_id):
    """This function checks whether the user 
    with auth_user_id is a student of the course: course_id
    """
    try:
        course_student = db.session.get(CourseStudent, (course_id, auth_user_id))
    except SQLAlchemyError:
        # every exception should result in a rollback
        db.session.rollback()
        abort(make_response(({"message": "An error occurred while fetching the user",
                    "url": f"{API_URL}/users"}, 500)))
    if course_student:
        return True
    return False


def get_course_of_project(project_id):
    """This function returns the course_id of the course associated with the project: project_id"""
    project = get_project(project_id)
    return project.course_id


def project_visible(project_id):
    """Determine whether a project is visible for students"""
    project = get_project(project_id)
    return project.visible_for_students


def get_course_of_submission(submission_id):
    """Get the course linked to a given submission"""
    submission = get_submission(submission_id)
    return get_course_of_project(submission.project_id)


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


def authorize_admin(f):
    """
    This function will check if the person sending a request to the API is logged in and an admin.
    Returns 403: Not Authorized if either condition is false
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        if is_admin(auth_user_id):
            return f(*args, **kwargs)
        abort(make_response(({"message":
                           """You are not authorized to perfom this action,
                             only admins are authorized"""}, 403)))
    return wrap


def authorize_teacher(f):
    """
    This function will check if the person sending a request to the API is logged in and a teacher.
    Returns 403: Not Authorized if either condition is false
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        if is_teacher(auth_user_id):
            kwargs["teacher_id"] = auth_user_id
            return f(*args, **kwargs)
        abort(make_response(({"message":
                           """You are not authorized to perfom this action,
                             only teachers are authorized"""}, 403)))
    return wrap


def authorize_teacher_of_course(f):
    """
    This function will check if the person sending a request to the API is logged in, 
    and the teacher of the course in the request.
    Returns 403: Not Authorized if either condition is false
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        if is_teacher_of_course(auth_user_id, kwargs["course_id"]):
            return f(*args, **kwargs)

        abort(make_response(({"message":"You're not authorized to perform this action"}, 403)))
    return wrap


def authorize_teacher_or_course_admin(f):
    """
    This function will check if the person sending a request to the API is logged in, 
    and the teacher of the course in the request or an admin of this course.
    Returns 403: Not Authorized if either condition is false
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        course_id = kwargs["course_id"]
        if (is_teacher_of_course(auth_user_id, course_id)
            or is_admin_of_course(auth_user_id, course_id)):
            return f(*args, **kwargs)

        abort(make_response(({"message":"""You are not authorized to perfom this action,
                           only teachers and course admins are authorized"""}, 403)))
    return wrap


def authorize_user(f):
    """
    This function will check if the person sending a request to the API is logged in, 
    and the same user that the request is about.
    Returns 403: Not Authorized if either condition is false
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        user_id = kwargs["user_id"]
        if auth_user_id == user_id:
            return f(*args, **kwargs)

        abort(make_response(({"message":"""You are not authorized to perfom this action,
                            you are not this user"""}, 403)))
    return wrap


def authorize_teacher_of_project(f):
    """
    This function will check if the person sending a request to the API is logged in, 
    and the teacher of the course which the project in the request belongs to.
    Returns 403: Not Authorized if either condition is false
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        project_id = kwargs["project_id"]
        course_id = get_course_of_project(project_id)

        if is_teacher_of_course(auth_user_id, course_id):
            return f(*args, **kwargs)

        abort(make_response(({"message":"""You are not authorized to perfom this action,
                            you are not the teacher of this project"""}, 403)))
    return wrap


def authorize_teacher_or_project_admin(f):
    """
    This function will check if the person sending a request to the API is logged in, 
    and the teacher or an admin of the course which the project in the request belongs to.
    Returns 403: Not Authorized if either condition is false
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        project_id = kwargs["project_id"]
        course_id = get_course_of_project(project_id)
        if (is_teacher_of_course(auth_user_id, course_id)
            or is_admin_of_course(auth_user_id, course_id)):
            return f(*args, **kwargs)
        abort(make_response(({"message":"""You are not authorized to perfom this action,
                           you are not the teacher or an admin of this project"""}, 403)))
    return wrap


def authorize_project_visible(f):
    """
    This function will check if the person sending a request to the API is logged in, 
    and the teacher of the course which the project in the request belongs to.
    Or if the person is a student of this course, 
    it will return the project if it is visible for students.
    Returns 403: Not Authorized if either condition is false
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        project_id = kwargs["project_id"]
        course_id = get_course_of_project(project_id)
        if (is_teacher_of_course(auth_user_id, course_id)
            or is_admin_of_course(auth_user_id, course_id)):
            return f(*args, **kwargs)
        if is_student_of_course(auth_user_id, course_id) and project_visible(project_id):
            return f(*args, **kwargs)
        abort(make_response(({"message":"You're not authorized to perform this action"}, 403)))
    return wrap

def authorize_submissions_request(f):
    """This function will check if the person sending a request to the API is logged in,
    and either the teacher/admin of the course or the student
    that the submission belongs to
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        project_id = request.args["project_id"]
        course_id = get_course_of_project(project_id)

        if (is_teacher_of_course(auth_user_id, course_id)
            or is_admin_of_course(auth_user_id, course_id)):
            return f(*args, **kwargs)

        if (is_student_of_course(auth_user_id, course_id)
            and project_visible(project_id)
            and auth_user_id == request.args.get("uid")):
            return f(*args, **kwargs)
        abort(make_response(({"message":"You're not authorized to perform this action"}, 403)))
    return wrap


def authorize_student_submission(f):
    """This function will check if the person sending a request to the API is logged in,
    and a student of the course they're trying to post a submission to
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        project_id = request.form["project_id"]
        course_id = get_course_of_project(project_id)
        if (is_student_of_course(auth_user_id, course_id)
            and project_visible(project_id)
            and auth_user_id == request.form.get("uid")):
            return f(*args, **kwargs)
        abort(make_response(({"message":"You're not authorized to perform this action"}, 403)))
    return wrap


def authorize_submission_author(f):
    """This function will check if the person sending a request to the API is logged in,
    and the original author of the submission
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        submission_id = kwargs["submission_id"]
        submission = get_submission(submission_id)
        if submission.uid == auth_user_id:
            return f(*args, **kwargs)
        abort(make_response(({"message":"You're not authorized to perform this action"}, 403)))
    return wrap


def authorize_grader(f):
    """This function will check if the person sending a request to the API is logged in,
    and either the teacher/admin of the course.
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        course_id = get_course_of_submission(kwargs["submission_id"])
        if (is_teacher_of_course(auth_user_id, course_id)
            or is_admin_of_course(auth_user_id, course_id)):
            return f(*args, **kwargs)
        abort(make_response(({"message":"You're not authorized to perform this action"}, 403)))
    return wrap


def authorize_submission_request(f):
    """This function will check if the person sending a request to the API is logged in,
    and either the teacher/admin of the course or the student
    that the submission belongs to
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        submission_id = kwargs["submission_id"]
        submission = get_submission(submission_id)
        if submission.uid == auth_user_id:
            return f(*args, **kwargs)
        course_id = get_course_of_project(submission.project_id)
        if (is_teacher_of_course(auth_user_id, course_id)
            or is_admin_of_course(auth_user_id, course_id)):
            return f(*args, **kwargs)
        abort(make_response(({"message":
                              "You're not authorized to perform this action"}
                              , 403)))
    return wrap
