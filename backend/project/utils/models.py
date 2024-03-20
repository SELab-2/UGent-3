"""This module contains helper functions for accessing the database"""

from os import getenv

from dotenv import load_dotenv

from flask import abort, make_response

from sqlalchemy.exc import SQLAlchemyError

from project import db

from project.models.user import User
from project.models.course import Course
from project.models.project import Project
from project.models.submission import Submission

load_dotenv()
API_URL = getenv("API_HOST")


def get_course(course_id):
    """Returns the course associated with course_id or the appropriate error"""
    try:
        course = db.session.get(Course, course_id)
    except SQLAlchemyError:
    # every exception should result in a rollback
        db.session.rollback()
        abort(make_response(({"message": "An error occurred while fetching the user",
                    "url": f"{API_URL}/users"}, 500)))

    if not course:
        abort(make_response(({"message":f"Course with id: {course_id} not found"}, 404)))
    return course


def get_project(project_id):
    """Returns the project associated with project_id or the appropriate error"""
    if isinstance(project_id, str) and not project_id.isnumeric():
        abort(make_response(({"message": f"{project_id} is not a valid project id"}
                             , 400)))
    try:
        project = db.session.get(Project, project_id)
    except SQLAlchemyError:
    # every exception should result in a rollback
        db.session.rollback()
        abort(make_response(({"message": "An error occurred while fetching the project"}
                             , 500)))

    if not project:
        abort(make_response(({"message":f"Project with id: {project_id} not found"}, 404)))

    return project


def get_submission(submission_id):
    """Returns the submission associated with submission_id or the appropriate error"""
    try:
        submission = db.session.get(Submission, submission_id)
    except SQLAlchemyError:
    # every exception should result in a rollback
        db.session.rollback()
        abort(make_response(({"message":"An error occurred while fetching the submission"}, 500)))

    if not submission:
        abort(make_response(({"message":f"Submission with id: {submission_id} not found"}, 404)))

    return submission


def get_user(user_id):
    """Returns the user associated with user_id or the appropriate error"""
    try:
        user = db.session.get(User, user_id)
    except SQLAlchemyError:
        # every exception should result in a rollback
        db.session.rollback()
        abort(make_response(({"message": "An error occurred while fetching the user"}
                            , 500)))
    if not user: # should realistically never happen
        abort(make_response(({"message":f"User with id: {user_id} not found"}, 404)))
    return user
