"""
This module contains the API endpoint for the submission detail
"""

from os import getenv
from urllib.parse import urljoin
from flask import request
from flask_restful import Resource
from sqlalchemy import exc
from project.db_in import db
from project.models.submission import Submission
from project.utils.models.submission_utils import submission_response
from project.utils.authentication import (
    authorize_submission_request,
    authorize_grader
)

API_HOST = getenv("API_HOST")
UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")
BASE_URL =  urljoin(f"{API_HOST}/", "/submissions")

class SubmissionEndpoint(Resource):
    """API endpoint for the submission"""

    @authorize_submission_request
    def get(self, submission_id: int) -> dict[str, any]:
        """Get the submission given an submission ID

        Args:
            submission_id (int): Submission ID

        Returns:
            dict[str, any]: The submission
        """

        data = {
            "url": urljoin(f"{BASE_URL}/", str(submission_id))
        }
        try:
            with db.session() as session:
                submission = session.get(Submission, submission_id)
                if submission is None:
                    data["url"] = urljoin(f"{API_HOST}/", "/submissions")
                    data["message"] = f"Submission (submission_id={submission_id}) not found"
                    return data, 404

                if set(request.form.keys()) - {"grading", "submission_id", "uid", "project_id", "submission_time"}:
                    data["message"] = "Invalid data field given."
                    return data, 400

                return {
                    "data": {
                        "submission_id": urljoin(f"{BASE_URL}/",  str(submission.submission_id)),
                        "uid": urljoin(f"{API_HOST}/", f"/users/{str(submission.uid)}"),
                        "project_id": urljoin(
                            f"{API_HOST}/",
                            f"/projects/{str(submission.project_id)}"),
                        "grading": submission.grading,
                        "submission_time": submission.submission_time,
                        "submission_status": submission.submission_status
                        },
                    "message": "Successfully fetched the submission",
                    "url": urljoin(f"{BASE_URL}/", str(submission.submission_id))
                }, 200

        except exc.SQLAlchemyError:
            data["message"] = \
                f"An error occurred while fetching the submission (submission_id={submission_id})"
            return data, 500

    @authorize_grader
    def patch(self, submission_id:int) -> dict[str, any]:
        """Update some fields of a submission given a submission ID

        Args:
            submission_id (int): Submission ID

        Returns:
            dict[str, any]: A message
        """

        data = {
            "url": urljoin(f"{BASE_URL}/", str(submission_id))
        }
        try:
            with db.session() as session:
                # Get the submission
                submission = session.get(Submission, submission_id)
                if submission is None:
                    data["url"] = urljoin(f"{API_HOST}/", "/submissions")
                    data["message"] = f"Submission (submission_id={submission_id}) not found"
                    return data, 404

                # Update the grading field
                if set(request.form.keys()) - {"grading"}:
                    data["message"] = "Invalid data field given, only 'grading' is allowed"
                    return data, 400

                grading = request.form.get("grading")
                if grading is not None:
                    try:
                        grading_float = float(grading)
                        if 0 <= grading_float <= 20:
                            submission.grading = grading_float
                        else:
                            data["message"] = "Invalid grading (grading=0-20)"
                            return data, 400
                    except ValueError:
                        data["message"] = "Invalid grading (not a valid float)"
                        return data, 400

                # Save the submission
                session.commit()

                data["message"] = f"Submission (submission_id={submission_id}) patched"
                data["url"] = urljoin(f"{BASE_URL}/", str(submission.submission_id))
                data["data"] = submission_response(submission, API_HOST)
                return data, 200

        except exc.SQLAlchemyError:
            session.rollback()
            data["message"] = \
                f"An error occurred while patching submission (submission_id={submission_id})"
            return data, 500
