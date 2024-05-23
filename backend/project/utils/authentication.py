"""
This module contains the functions to authenticate API calls.
"""
from os import getenv

from functools import wraps

from dotenv import load_dotenv

from flask import abort, request, make_response
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from project.utils.models.course_utils import is_admin_of_course, \
    is_student_of_course, is_teacher_of_course
from project.utils.models.project_utils import get_course_of_project, project_visible
from project.utils.models.submission_utils import get_submission, get_course_of_submission
from project.utils.models.user_utils import get_user

load_dotenv()
API_URL = getenv("API_HOST")
AUTHENTICATION_URL = getenv("AUTHENTICATION_URL")


def not_allowed(f):
    """Decorator function to immediately abort the current request and return 403: Forbidden"""
    @wraps(f)
    def wrap(*args, **kwargs):
        return {"message": "Forbidden action"}, 403
    return wrap


def return_authenticated_user_id():
    """This function will authenticate the request and ensure the user was added to the database,
    otherwise it will prompt them to login again
    """
    verify_jwt_in_request()
    uid = get_jwt_identity()
    get_user(uid)
    return uid


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


def login_required_return_uid(f):
    """
    This function will check if the person sending a request to the API is logged in
    and additionally create their user entry in the database if necessary
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        uid = return_authenticated_user_id()
        kwargs["uid"] = uid
        return f(*args, **kwargs)
    return wrap


def authorize_admin(f):
    """
    This function will check if the person sending a request to the API is logged in and an admin.
    Returns 403: Not Authorized if either condition is false
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        return_authenticated_user_id()
        if get_jwt()["is_admin"]:
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
        if get_jwt()["is_teacher"]:
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

        abort(make_response(
            ({"message": "You're not authorized to perform this action"}, 403)))
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

        abort(make_response(({"message": """You are not authorized to perfom this action,
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

        abort(make_response(({"message": """You are not authorized to perfom this action,
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

        abort(make_response(({"message": """You are not authorized to perfom this action,
                            you are not the teacher of this project"""}, 403)))
    return wrap


def authorize_teacher_or_student_of_project(f):
    """
    This function will check if the person sending a request to the API is logged in, 
    and the teacher or student of the course which the project in the request belongs to.
    Returns 403: Not Authorized if either condition is false
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        project_id = kwargs["project_id"]
        course_id = get_course_of_project(project_id)

        if (is_teacher_of_course(auth_user_id, course_id) or
            is_student_of_course(auth_user_id, course_id)):
            return f(*args, **kwargs)

        abort(make_response(({"message": """You are not authorized to perfom this action,
                            you are not the teacher OR student of this project"""}, 403)))
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
        abort(make_response(({"message": """You are not authorized to perfom this action,
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
        abort(make_response(
            ({"message": "You're not authorized to perform this action"}, 403)))
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
        abort(make_response(
            ({"message": "You're not authorized to perform this action"}, 403)))
    return wrap


def authorize_student_submission(f):
    """This function will check if the person sending a request to the API is logged in,
    and a student of the course they're trying to post a submission to
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_user_id = return_authenticated_user_id()
        kwargs["uid"] = auth_user_id
        project_id = request.form["project_id"]
        course_id = get_course_of_project(project_id)
        if (is_student_of_course(auth_user_id, course_id) and project_visible(project_id)):
            return f(*args, **kwargs)
        abort(make_response(
            ({"message": "You're not authorized to perform this action"}, 403)))
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
        abort(make_response(
            ({"message": "You're not authorized to perform this action"}, 403)))
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
        abort(make_response(
            ({"message": "You're not authorized to perform this action"}, 403)))
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
                              "You're not authorized to perform this action"}, 403)))
    return wrap
