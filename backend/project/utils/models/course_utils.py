"""This module contains helper functions related to courses for accessing the database"""

from os import getenv

from dotenv import load_dotenv

from flask import abort, make_response
from sqlalchemy.exc import SQLAlchemyError

from project import db
from project.models.course import Course
from project.models.course_relation import CourseAdmin, CourseStudent

load_dotenv()
API_URL = getenv("API_HOST")

def get_course(course_id):
    """Returns the course associated with course_id or the appropriate error"""
    try:
        course = db.session.get(Course, course_id)
    except SQLAlchemyError:
        db.session.rollback()
        abort(make_response(({"message": "An error occurred while fetching the user",
                    "url": f"{API_URL}/users"}, 500)))

    if not course:
        abort(make_response(({"message":f"Course with id: {course_id} not found"}, 404)))
    return course

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
        db.session.rollback()
        abort(make_response(({"message": "An error occurred while fetching the user",
                    "url": f"{API_URL}/users"}, 500)))
    if course_student:
        return True
    return False
