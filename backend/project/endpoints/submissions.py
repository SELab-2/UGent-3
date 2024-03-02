"""Submission API endpoint"""

from datetime import datetime
from os import getenv
from flask import Blueprint, request
from flask_restful import Resource
from sqlalchemy import exc
from project.database import db
from project.models.submissions import Submissions as m_submissions
from project.models.projects import Projects as m_projects
from project.models.users import Users as m_users

submissions_bp = Blueprint("submissions", __name__)

class Submissions(Resource):
    """API endpoint for the submissions"""

    def get(self) -> dict[str, any]:
        """Get all the submissions from a user for a project

        Returns:
            dict[str, any]: The list of submission URLs
        """

        data = {}
        try:
            with db.session() as session:
                query = session.query(m_submissions)

                # Filter by uid
                uid = request.args.get("uid")
                if uid is not None:
                    if session.get(m_users, uid) is not None:
                        query = query.filter_by(uid=uid)
                    else:
                        data["message"] = f"Invalid user (uid={uid})"
                        return data, 400

                # Filter by project_id
                project_id = request.args.get("project_id")
                if project_id is not None:
                    if session.get(m_projects, project_id) is not None:
                        query = query.filter_by(project_id=project_id)
                    else:
                        data["message"] = f"Invalid project (project_id={project_id})"
                        return data, 400

                # Get the submissions
                data["message"] = "Successfully fetched the submissions"
                data["submissions"] = [
                    f"{getenv('HOSTNAME')}/submissions/{s.submission_id}" for s in query.all()
                ]
                return data, 200

        except exc.SQLAlchemyError:
            data["message"] = "An error occurred while fetching the submissions"
            return data, 500

    def post(self) -> dict[str, any]:
        """Post a new submission to a project

        Returns:
            dict[str, any]: The URL to the submission
        """

        data = {}
        try:
            with db.session() as session:
                submission = m_submissions()

                # User
                uid = request.form.get("uid")
                if (uid is None) or (session.get(m_users, uid) is None):
                    if uid is None:
                        data["message"] = "The uid data field is required"
                    else:
                        data["message"] = f"Invalid user (uid={uid})"
                    return data, 400
                submission.uid = uid

                # Project
                project_id = request.form.get("project_id")
                if (project_id is None) or (session.get(m_projects, project_id) is None):
                    if project_id is None:
                        data["message"] = "The project_id data field is required"
                    else:
                        data["message"] = f"Invalid project (project_id={project_id})"
                    return data, 400
                submission.project_id = project_id

                # Grading
                grading = int(request.form.get("grading"))
                if grading is not None:
                    if not 0 <= grading <= 20:
                        data["message"] = "Invalid grading (range=0-20)"
                        return data, 400
                    submission.grading = grading

                # Submission time
                submission.submission_time = datetime.now()

                # Submission path
                # Get the files, store them, test them ...
                submission.submission_path = "/tbd"

                # Submission status
                submission.submission_status = False

                session.add(submission)
                session.commit()

                data["message"] = "Successfully fetched the submissions"
                data["submission"] = f"{getenv('HOSTNAME')}/submissions/{submission.submission_id}"
                return data, 201

        except exc.SQLAlchemyError:
            session.rollback()
            data["message"] = "An error occurred while creating a new submission"
            return data, 500

class Submission(Resource):
    """API endpoint for the submission"""

    def get(self, submission_id: int) -> dict[str, any]:
        """Get the submission given an submission ID

        Args:
            submission_id (int): Submission ID

        Returns:
            dict[str, any]: The submission
        """

        data = {}
        try:
            with db.session() as session:
                submission = session.get(m_submissions, submission_id)
                if submission is None:
                    data["message"] = f"Submission (submission_id={submission_id}) not found"
                    return data, 404

                data["message"] = "Successfully fetched the submission"
                data["submission"] = {
                    "submission_id": submission.submission_id,
                    "uid": submission.uid,
                    "project_id": submission.project_id,
                    "grading": submission.grading,
                    "submission_time": submission.submission_time,
                    "submission_path": submission.submission_path,
                    "submission_status": submission.submission_status
                }
                return data, 200
        except exc.SQLAlchemyError:
            data["message"] = \
                f"An error occurred while fetching the submission (submission_id={submission_id})"
            return data, 500

    def patch(self, submission_id:int) -> dict[str, any]:
        """Update some fields of a submission given a submission ID

        Args:
            submission_id (int): Submission ID

        Returns:
            dict[str, any]: A message
        """

        try:
            with db.session() as session:
                # Get the submission
                submission = session.get(m_submissions, submission_id)
                if submission is None:
                    return {"message": f"Submission {submission_id} not found"}, 404

                # Update the grading field (its the only field that a teacher can update)
                if "grading" in request.form:
                    grading = request.form["grading"]
                    if grading < 0 or grading > 20:
                        return {
                            "message": "The submission must have a 'grading' in between 0-20"
                        }, 400
                    submission.grading = grading

                # Save the submission
                session.commit()
                return {"message": f"Submission {submission_id} updated"}
        except exc.SQLAlchemyError:
            session.rollback()
            return {"message": f"An error occurred while patching submission {submission_id}"}, 500

    def delete(self, submission_id: int) -> dict[str, any]:
        """Delete a submission given an submission ID

        Args:
            submission_id (int): Submission ID

        Returns:
            dict[str, any]: A message
        """

        try:
            with db.session() as session:
                # Check if the submission exists
                submission = session.get(m_submissions, submission_id)
                if submission is None:
                    return {"message": f"Submission {submission_id} not found"}, 404

                # Delete the submission
                session.delete(submission)
                session.commit()
                return {"message": f"Submission {submission_id} deleted"}
        except exc.SQLAlchemyError:
            db.session.rollback()
            return {"message": f"An error occurred while deleting submission {submission_id}"}, 500

submissions_bp.add_url_rule("/submissions", view_func=Submissions.as_view("submissions"))
submissions_bp.add_url_rule(
    "/submissions/<int:submission_id>",
    view_func=Submission.as_view("submission")
)
