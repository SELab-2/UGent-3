"""Submission API endpoint"""

from datetime import datetime
from flask import Blueprint, request
from flask_restful import Resource
from project.database import db
from project.models.submissions import Submissions as m_submissions
from project.models.projects import Projects as m_projects
from project.models.users import Users as m_users

submissions_bp = Blueprint("submissions", __name__)

class Submissions(Resource):
    """API endpoint for the submissions"""

    def get(self, uid: str, pid: int) -> dict[str, any]:
        """Get all the submissions from a user for a project

        Args:
            uid (str): User ID
            pid (int): Project ID

        Returns:
            dict[str, any]: The list of submission URLs
        """

        # Authentication
        # uid_operator = 0
        # if uid_operator is None:
        #     return {"message": "Not logged in"}, 401

        try:
            with db.session() as session:
                # Authorization
                # operator = session.get(m_users, uid_operator)
                # if operator is None:
                #     return {"message": f"User {uid_operator} not found"}, 404
                # if not (operator.is_admin or operator.is_teacher or uid_operator == uid):
                #     return {"message": f"User {uid_operator} does not have the correct rights"}, 403

                # Check user
                user = session.get(m_users, uid)
                if user is None:
                    return {"message": f"User {uid} not found"}, 404

                # Check project
                project = session.get(m_projects, pid)
                if project is None:
                    return {"message": f"Project {pid} not found"}, 404

                # Get the submissions
                submissions = session.query(m_submissions).filter_by(uid=uid, project_id=pid).all()
                submissions_urls = [f"/submissions/{s.submission_id}" for s in submissions]
                return {"submissions": submissions_urls}
        except Exception:
            return {"message": f"An error occurred while fetching the submissions from user {uid} for project {pid}"}, 500

    def post(self, uid: str, pid: int) -> dict[str, any]:
        """Post a new submission to a project

        Args:
            uid (str): User ID
            pid (int): Project ID

        Returns:
            dict[str, any]: The URL to the submission
        """

        # Authentication
        # uid_operator = 0
        # if uid_operator is None:
        #     return {"message": "Not logged in"}, 401

        try:
            with db.session() as session:
                # Authorization
                # operator = session.get(m_users, uid_operator)
                # if operator is None:
                #     return {"message": f"User {uid_operator} not found"}, 404
                # if uid_operator != uid:
                #     return {"message": f"User {uid_operator} does not have the correct rights"}, 403

                submission = m_submissions()

                # User
                user = session.get(m_users, uid)
                if user is None:
                    return {"message": f"User {uid} not found"}, 404
                submission.uid = uid

                # Project
                project = session.get(m_projects, pid)
                if project is None:
                    return {"message": f"Project {pid} not found"}, 404
                submission.project_id = pid

                # Grading
                if "grading" in request.form:
                    grading = request.form["grading"]
                    if grading < 0 or grading > 20:
                        return {"message": "The submission must have a 'grading' in between 0 and 20"}, 400
                    submission.grading = grading

                # Submission time
                submission.submission_time = datetime.now()

                # Submission path
                # get the files and store them
                submission.submission_path = "/tbd"

                # Submission status
                submission.submission_status = False

                session.add(submission)
                session.commit()
                return {"submission": f"/submissions/{submission.submission_id}"}, 201
        except Exception:
            session.rollback()
            return {"message": f"An error occurred while creating a new submission for user {uid} in project {pid}"}, 500

submissions_bp.add_url_rule(
    "/submissions/<string:uid>/<int:pid>",
    view_func=Submissions.as_view("submissions"))

class Submission(Resource):
    """API endpoint for the submission"""

    def get(self, sid: int) -> dict[str, any]:
        """Get the submission given an submission ID

        Args:
            sid (int): Submission ID

        Returns:
            dict[str, any]: The submission
        """

        # Authentication
        # uid_operator = 0
        # if uid_operator is None:
        #     return {"message": "Not logged in"}, 401

        try:
            with db.session() as session:
                # Authorization
                # operator = session.get(m_users, uid_operator)
                # if operator is None:
                #     return {"message": f"User {uid_operator} not found"}, 404
                # if not (operator.is_admin or operator.is_teacher or uid_operator == uid):
                #     return {"message": f"User {uid_operator} does not have the correct rights"}, 403

                # Get the submission
                submission = session.get(m_submissions, sid)
                if submission is None:
                    return {"message": f"Submission {sid} not found"}, 404

                return {
                    "submission_id": submission.submission_id,
                    "uid": submission.uid,
                    "project_id": submission.project_id,
                    "grading": submission.grading,
                    "submission_time": submission.submission_time,
                    "submission_path": submission.submission_path,
                    "submission_status": submission.submission_status
                }
        except Exception:
            return {"message": f"An error occurred while fetching submission {sid}"}, 500

    def patch(self, sid:int) -> dict[str, any]:
        """Update some fields of a submission given a submission ID

        Args:
            sid (int): Submission ID

        Returns:
            dict[str, any]: A message
        """

        # Authentication
        # uid_operator = 0
        # if uid_operator is None:
        #     return {"message": "Not logged in"}, 401

        try:
            with db.session() as session:
                # Authorization
                # operator = session.get(m_users, uid_operator)
                # if operator is None:
                #     return {"message": f"User {uid_operator} not found"}, 404
                # if not operator.is_teacher:
                #     return {"message": f"User {uid_operator} does not have the correct rights"}, 403

                # Get the submission
                submission = session.get(m_submissions, sid)
                if submission is None:
                    return {"message": f"Submission {sid} not found"}, 404

                # Update the grading field (its the only field that a teacher can update)
                if "grading" in request.form:
                    grading = request.form["grading"]
                    if grading < 0 or grading > 20:
                        return {"message": "The submission must have a 'grading' in between 0 and 20"}, 400
                    submission.grading = grading

                # Save the submission
                session.commit()
                return {"message": "Submission {sid} updated"}
        except Exception:
            session.rollback()
            return {"message": f"An error occurred while patching submission {sid}"}, 500

    def delete(self, sid: int) -> dict[str, any]:
        """Delete a submission given an submission ID

        Args:
            sid (int): Submission ID

        Returns:
            dict[str, any]: A message
        """

        # Authentication
        # uid_operator = 0
        # if uid_operator is None:
        #     return {"message": "Not logged in"}, 401

        try:
            with db.session() as session:
                # Authorization
                # operator = session.get(m_users, uid_operator)
                # if operator is None:
                #     return {"message": f"User {uid_operator} not found"}, 404
                # if not operator.is_admin:
                #     return {"message": f"User {uid_operator} does not have the correct rights"}, 403

                # Check if the submission exists
                submission = session.get(m_submissions, sid)
                if submission is None:
                    return {"message": f"Submission {sid} not found"}, 404

                # Delete the submission
                session.delete(submission)
                session.commit()
                return {"message": f"Submission {sid} deleted"}
        except Exception:
            db.session.rollback()
            return {"message": f"An error occurred while deleting submission {sid}"}, 500

submissions_bp.add_url_rule(
    "/submissions/<int:sid>",
    view_func=Submission.as_view("submission"))
