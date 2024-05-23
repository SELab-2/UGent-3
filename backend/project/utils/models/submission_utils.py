"""This module contains helper functions related to submissions for accessing the database"""

from os import getenv

from dotenv import load_dotenv

from flask import abort, make_response
from sqlalchemy.exc import SQLAlchemyError

from project import db
from project.models.submission import Submission
from project.utils.models.project_utils import get_course_of_project

load_dotenv()
API_URL = getenv("API_HOST")

def get_submission(submission_id):
    """Returns the submission associated with submission_id or the appropriate error"""
    try:
        submission = db.session.get(Submission, submission_id)
    except SQLAlchemyError:
        db.session.rollback()
        abort(make_response(({"message":"An error occurred while fetching the submission"}, 500)))

    if not submission:
        abort(make_response(({"message":f"Submission with id: {submission_id} not found"}, 404)))

    return submission

def get_course_of_submission(submission_id):
    """Get the course linked to a given submission"""
    submission = get_submission(submission_id)
    return get_course_of_project(submission.project_id)

def submission_response(submission, api_host):
    """Return the response data for a submission"""
    return {
        "submission_id": f"{api_host}/submissions/{submission.submission_id}",
        "uid": f"{api_host}/users/{submission.uid}",
        "project_id": f"{api_host}/projects/{submission.project_id}",
        "grading": submission.grading,
        "submission_time": submission.submission_time,
        "submission_status": submission.submission_status
    }
