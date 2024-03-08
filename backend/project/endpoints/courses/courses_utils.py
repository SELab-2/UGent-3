"""
This module contains utility functions for the courses endpoints.
The functions are used to interact with the database and handle errors.
"""

from os import getenv
from urllib.parse import urljoin

from dotenv import load_dotenv
from flask import abort
from sqlalchemy.exc import SQLAlchemyError

from project import db
from project.models.course_relations import CourseAdmin
from project.models.users import User
from project.models.courses import Course

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(API_URL + "/", "courses")

def execute_query_abort_if_db_error(query, url, query_all=False):
    """
    Execute the given SQLAlchemy query and handle any SQLAlchemyError that might occur.
    If query_all == True, the query will be executed with the all() method,
    otherwise with the first() method.
    Args:
        query (Query): The SQLAlchemy query to execute.

    Returns:
        ResultProxy: The result of the query if successful, otherwise aborts with error 500.
    """
    try:
        if query_all:
            result = query.all()
        else:
            result = query.first()
    except SQLAlchemyError as e:
        response = json_message(str(e))
        response["url"] = url
        abort(500, description=response)
    return result


def add_abort_if_error(to_add, url):
    """
    Add a new object to the database
    and handle any SQLAlchemyError that might occur.

    Args:
        to_add (object): The object to add to the database.
    """
    try:
        db.session.add(to_add)
    except SQLAlchemyError as e:
        db.session.rollback()
        response = json_message(str(e))
        response["url"] = url
        abort(500, description=response)


def delete_abort_if_error(to_delete, url):
    """
    Deletes the given object from the database
    and aborts the request with a 500 error if a SQLAlchemyError occurs.

    Args:
    - to_delete: The object to be deleted from the database.
    """
    try:
        db.session.delete(to_delete)
    except SQLAlchemyError as e:
        db.session.rollback()
        response = json_message(str(e))
        response["url"] = url
        abort(500, description=response)


def commit_abort_if_error(url):
    """
    Commit the current session and handle any SQLAlchemyError that might occur.
    """
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        response = json_message(str(e))
        response["url"] = url
        abort(500, description=response)


def abort_if_not_teacher_or_none_assistant(course_id, teacher, assistant):
    """
    Check if the current user is authorized to appoint new admins to a course.

    Args:
        course_id (int): The ID of the course.

    Raises:
        HTTPException: If the current user is not authorized or
        if the UID of the person to be made an admin is missing in the request body.
    """
    url = f"{API_URL}/courses/{str(course_id)}/admins"
    abort_if_uid_is_none(teacher, url)

    course = get_course_abort_if_not_found(course_id)

    if teacher != course.teacher:
        response = json_message("Only the teacher of a course can appoint new admins")
        response["url"] = url
        abort(403, description=response)

    if not assistant:
        response = json_message(
            "uid of person to make admin is required in the request body"
        )
        response["url"] = url
        abort(400, description=response)


def abort_if_none_uid_student_uids_or_non_existant_course_id(
    course_id, uid, student_uids
):
    """
    Check the request to assign new students to a course.

    Args:
        course_id (int): The ID of the course.

    Raises:
        403: If the user is not authorized to assign new students to the course.
        400: If the request body does not contain the required 'students' field.
    """
    url = f"{API_URL}/courses/{str(course_id)}/students"
    get_course_abort_if_not_found(course_id)
    abort_if_no_user_found_for_uid(uid, url)
    query = CourseAdmin.query.filter_by(uid=uid, course_id=course_id)
    admin_relation = execute_query_abort_if_db_error(query, url)
    if not admin_relation:
        message = "Not authorized to assign new students to course with id " + str(
            course_id
        )
        response = json_message(message)
        response["url"] = url
        abort(403, description=response)

    if not student_uids:
        message = """To assign new students to a course,
                     you should have a students field with a list of uids in the request body"""
        response = json_message(message)
        response["url"] = url
        abort(400, description=response)


def abort_if_uid_is_none(uid, url):
    """
    Check whether the uid is None if so
    abort with error 400
    """
    if uid is None:
        response = json_message("There should be a uid in the request query")
        response["url"] = url
        abort(400, description=response)


def abort_if_no_user_found_for_uid(uid, url):
    """
    Check if a user exists based on the provided uid.

    Args:
        uid (int): The unique identifier of the user.

    Raises:
        NotFound: If the user with the given uid is not found.
    """
    query = User.query.filter_by(uid=uid)
    user = execute_query_abort_if_db_error(query, url)

    if not user:
        response = json_message(f"User with uid {uid} was not found")
        response["url"] = url
        abort(404, description=response)
    return user


def get_admin_relation(uid, course_id):
    """
    Retrieve the CourseAdmin object for the given uid and course.

    Args:
        uid (int): The user ID.
        course_id (int): The course ID.

    Returns:
        CourseAdmin: The CourseAdmin object if the user is an admin, otherwise None.
    """
    return execute_query_abort_if_db_error(
        CourseAdmin.query.filter_by(uid=uid, course_id=course_id),
        url=f"{API_URL}/courses/{str(course_id)}/admins",
    )


def json_message(message):
    """
    Create a json message with the given message.

    Args:
        message (str): The message to include in the json.

    Returns:
        dict: The message in a json format.
    """
    return {"message": message}


def get_course_abort_if_not_found(course_id):
    """
    Get a course by its ID.

    Args:
        course_id (int): The course ID.

    Returns:
        Course: The course with the given ID.
    """
    query = Course.query.filter_by(course_id=course_id)
    course = execute_query_abort_if_db_error(query, f"{API_URL}/courses")

    if not course:
        response = json_message("Course not found")
        response["url"] = f"{API_URL}/courses"
        abort(404, description=response)

    return course