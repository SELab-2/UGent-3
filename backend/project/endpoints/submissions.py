"""Submission API endpoint"""

from urllib.parse import urljoin
from datetime import datetime
from os import getenv, path
from dotenv import load_dotenv
from flask import Blueprint, request
from flask_restful import Resource
from sqlalchemy import exc
from project.db_in import db
from project.models.submission import Submission
from project.models.project import Project
from project.models.user import User
from project.utils.files import filter_files, all_files_uploaded, zip_files
from project.utils.user import is_valid_user
from project.utils.project import is_valid_project

load_dotenv()
API_HOST = getenv("API_HOST")
UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")

submissions_bp = Blueprint("submissions", __name__)

class SubmissionsEndpoint(Resource):
    """API endpoint for the submissions"""

    def get(self) -> dict[str, any]:
        """Get all the submissions from a user for a project

        Returns:
            dict[str, any]: The list of submission URLs
        """

        data = {
            "url": urljoin(f"{API_HOST}/", "/submissions")
        }
        try:
            with db.session() as session:
                query = session.query(Submission)

                # Filter by uid
                uid = request.args.get("uid")
                if uid is not None:
                    if session.get(User, uid) is not None:
                        query = query.filter_by(uid=uid)
                    else:
                        data["message"] = f"Invalid user (uid={uid})"
                        return data, 400

                # Filter by project_id
                project_id = request.args.get("project_id")
                if project_id is not None:
                    if not project_id.isdigit() or session.get(Project, int(project_id)) is None:
                        data["message"] = f"Invalid project (project_id={project_id})"
                        return data, 400
                    query = query.filter_by(project_id=int(project_id))

                # Get the submissions
                data["message"] = "Successfully fetched the submissions"
                data["data"] = [
                    urljoin(f"{API_HOST}/", f"/submissions/{s.submission_id}") for s in query.all()
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

        data = {
            "url": urljoin(f"{API_HOST}/", "/submissions")
        }
        try:
            with db.session() as session:
                submission = Submission()

                # User
                uid = request.form.get("uid")
                valid, message = is_valid_user(session, uid)
                if not valid:
                    data["message"] = message
                    return data, 400
                submission.uid = uid

                # Project
                project_id = request.form.get("project_id")
                valid, message = is_valid_project(session, project_id)
                if not valid:
                    data["message"] = message
                    return data, 400
                submission.project_id = int(project_id)

                # Submission time
                submission.submission_time = datetime.now()

                # Submission path
                files = filter_files(request.files.getlist("files"))
                project = session.get(Project, submission.project_id)
                if not files or not all_files_uploaded(files, project.regex_expressions):
                    data["message"] = "No files were uploaded" if not files else \
                        "Not all required files were uploaded"
                    return data, 400

                # Zip the files and save the zip
                zip_file = zip_files("", files)
                if zip_file is None:
                    data["message"] = "Something went wrong while zipping the files"
                    return data, 500
                submission.submission_path = "/zip.zip"
                zip_file.save(path.join(f"{UPLOAD_FOLDER}/", submission.submission_path))

                # Submission status
                submission.submission_status = False

                session.add(submission)
                session.commit()

                data["message"] = "Successfully fetched the submissions"
                data["url"] = urljoin(f"{API_HOST}/", f"/submissions/{submission.submission_id}")
                data["data"] = {
                    "id": submission.submission_id,
                    "user": urljoin(f"{API_HOST}/", f"/users/{submission.uid}"),
                    "project": urljoin(f"{API_HOST}/", f"/projects/{submission.project_id}"),
                    "grading": submission.grading,
                    "time": submission.submission_time,
                    "path": submission.submission_path,
                    "status": submission.submission_status
                }
                return data, 201

        except exc.SQLAlchemyError:
            session.rollback()
            data["message"] = "An error occurred while creating a new submission"
            return data, 500

class SubmissionEndpoint(Resource):
    """API endpoint for the submission"""

    def get(self, submission_id: int) -> dict[str, any]:
        """Get the submission given an submission ID

        Args:
            submission_id (int): Submission ID

        Returns:
            dict[str, any]: The submission
        """

        data = {
            "url": urljoin(f"{API_HOST}/", f"/submissions/{submission_id}")
        }
        try:
            with db.session() as session:
                submission = session.get(Submission, submission_id)
                if submission is None:
                    data["url"] = urljoin(f"{API_HOST}/", "/submissions")
                    data["message"] = f"Submission (submission_id={submission_id}) not found"
                    return data, 404

                data["message"] = "Successfully fetched the submission"
                data["data"] = {
                    "id": submission.submission_id,
                    "user": urljoin(f"{API_HOST}/", f"/users/{submission.uid}"),
                    "project": urljoin(f"{API_HOST}/", f"/projects/{submission.project_id}"),
                    "grading": submission.grading,
                    "time": submission.submission_time,
                    "path": submission.submission_path,
                    "status": submission.submission_status
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

        data = {
            "url": urljoin(f"{API_HOST}/", f"/submissions/{submission_id}")
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
                grading = request.form.get("grading")
                if grading is not None:
                    if not (grading.isdigit() and 0 <= int(grading) <= 20):
                        data["message"] = "Invalid grading (grading=0-20)"
                        return data, 400
                    submission.grading = int(grading)

                # Save the submission
                session.commit()

                data["message"] = f"Submission (submission_id={submission_id}) patched"
                data["url"] = urljoin(f"{API_HOST}/", f"/submissions/{submission.submission_id}")
                data["data"] = {
                    "id": submission.submission_id,
                    "user": urljoin(f"{API_HOST}/", f"/users/{submission.uid}"),
                    "project": urljoin(f"{API_HOST}/", f"/projects/{submission.project_id}"),
                    "grading": submission.grading,
                    "time": submission.submission_time,
                    "path": submission.submission_path,
                    "status": submission.submission_status
                }
                return data, 200

        except exc.SQLAlchemyError:
            session.rollback()
            data["message"] = \
                f"An error occurred while patching submission (submission_id={submission_id})"
            return data, 500

    def delete(self, submission_id: int) -> dict[str, any]:
        """Delete a submission given a submission ID

        Args:
            submission_id (int): Submission ID

        Returns:
            dict[str, any]: A message
        """

        data = {
            "url": urljoin(f"{API_HOST}/", "/submissions")
        }
        try:
            with db.session() as session:
                submission = session.get(Submission, submission_id)
                if submission is None:
                    data["url"] = urljoin(f"{API_HOST}/", "/submissions")
                    data["message"] = f"Submission (submission_id={submission_id}) not found"
                    return data, 404

                # Delete the submission
                session.delete(submission)
                session.commit()

                data["message"] = f"Submission (submission_id={submission_id}) deleted"
                return data, 200

        except exc.SQLAlchemyError:
            db.session.rollback()
            data["message"] = \
                f"An error occurred while deleting submission (submission_id={submission_id})"
            return data, 500

submissions_bp.add_url_rule("/submissions", view_func=SubmissionsEndpoint.as_view("submissions"))
submissions_bp.add_url_rule(
    "/submissions/<int:submission_id>",
    view_func=SubmissionEndpoint.as_view("submission")
)
