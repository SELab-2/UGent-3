"""Submission API endpoint"""

from urllib.parse import urljoin
from datetime import datetime
from os import getenv, path, makedirs
from zoneinfo import ZoneInfo
from shutil import rmtree
from dotenv import load_dotenv
from flask import Blueprint, request
from flask_restful import Resource
from sqlalchemy import exc
from project.db_in import db
from project.models.submission import Submission, SubmissionStatus
from project.models.project import Project
from project.models.user import User
from project.utils.files import all_files_uploaded
from project.utils.user import is_valid_user
from project.utils.project import is_valid_project
from project.utils.query_agent import query_selected_from_model, delete_by_id_from_model
from project.utils.authentication import authorize_submission_request, \
    authorize_submissions_request, authorize_grader, \
        authorize_student_submission, authorize_submission_author

load_dotenv()
API_HOST = getenv("API_HOST")
UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")
BASE_URL =  urljoin(f"{API_HOST}/", "/submissions")

TIMEZONE = getenv("TIMEZONE", "GMT")

submissions_bp = Blueprint("submissions", __name__)

class SubmissionsEndpoint(Resource):
    """API endpoint for the submissions"""

    @authorize_submissions_request
    def get(self) -> dict[str, any]:
        """Get all the submissions from a user for a project

        Returns:
            dict[str, any]: The list of submission URLs
        """

        data = {
            "url": BASE_URL
        }
        try:
            # Filter by uid
            uid = request.args.get("uid")
            if uid is not None and (not uid.isdigit() or not User.query.filter_by(uid=uid).first()):
                data["message"] = f"Invalid user (uid={uid})"
                return data, 400

            # Filter by project_id
            project_id = request.args.get("project_id")
            if project_id is not None \
                and (not project_id.isdigit() or
                     not Project.query.filter_by(project_id=project_id).first()):
                data["message"] = f"Invalid project (project_id={project_id})"
                return data, 400
        except exc.SQLAlchemyError:
            data["message"] = "An error occurred while fetching the submissions"
            return data, 500

        return query_selected_from_model(
            Submission,
            urljoin(f"{API_HOST}/", "/submissions"),
            select_values=[
                "submission_id", "uid",
                "project_id", "grading",
                "submission_time", "submission_status"],
            url_mapper={
                "submission_id": BASE_URL,
                "project_id": urljoin(f"{API_HOST}/", "projects"),
                "uid": urljoin(f"{API_HOST}/", "users")},
            filters=request.args
        )

    @authorize_student_submission
    def post(self) -> dict[str, any]:
        """Post a new submission to a project

        Returns:
            dict[str, any]: The URL to the submission
        """

        data = {
            "url": BASE_URL
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
                submission.submission_time = datetime.now(ZoneInfo(TIMEZONE))

                # Submission files
                submission.submission_path = "" # Must be set on creation
                files = request.files.getlist("files")

                # Check files otherwise stop
                project = session.get(Project, submission.project_id)
                if project.regex_expressions and \
                    (not files or not all_files_uploaded(files, project.regex_expressions)):
                    data["message"] = "No files were uploaded" if not files else \
                        "Not all required files were uploaded " \
                        f"(required files={','.join(project.regex_expressions)})"
                    return data, 400

                deadlines = project.deadlines
                submission.submission_status = SubmissionStatus.LATE
                for deadline in deadlines:
                    if submission.submission_time < deadline.deadline:
                        submission.submission_status = SubmissionStatus.RUNNING

                # Submission_id needed for the file location
                session.add(submission)
                session.commit()

                # Save the files
                submission.submission_path = path.join(UPLOAD_FOLDER, str(submission.project_id),
                    "submissions", str(submission.submission_id))
                try:
                    makedirs(submission.submission_path, exist_ok=True)
                    for file in files:
                        file.save(path.join(submission.submission_path, file.filename))
                    session.commit()
                except OSError:
                    rmtree(submission.submission_path)
                    session.rollback()

                data["message"] = "Successfully fetched the submissions"
                data["url"] = urljoin(f"{API_HOST}/", f"/submissions/{submission.submission_id}")
                data["data"] = {
                    "submission_id": urljoin(f"{BASE_URL}/",  str(submission.submission_id)),
                    "uid": urljoin(f"{API_HOST}/", f"/users/{submission.uid}"),
                    "project_id": urljoin(f"{API_HOST}/", f"/projects/{submission.project_id}"),
                    "grading": submission.grading,
                    "submission_time": submission.submission_time,
                    "submission_status": submission.submission_status
                }
                return data, 201

        except exc.SQLAlchemyError:
            session.rollback()
            data["message"] = "An error occurred while creating a new submission"
            return data, 500

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

                data["message"] = "Successfully fetched the submission"
                data["data"] = {
                    "submission_id": urljoin(f"{BASE_URL}/",  str(submission.submission_id)),
                    "uid": urljoin(f"{API_HOST}/", f"/users/{submission.uid}"),
                    "project_id": urljoin(f"{API_HOST}/", f"/projects/{submission.project_id}"),
                    "grading": submission.grading,
                    "submission_time": submission.submission_time,
                    "submission_status": submission.submission_status
                }
                return data, 200

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
                data["data"] = {
                    "id": urljoin(f"{BASE_URL}/",  str(submission.submission_id)),
                    "user": urljoin(f"{API_HOST}/", f"/users/{submission.uid}"),
                    "project": urljoin(f"{API_HOST}/", f"/projects/{submission.project_id}"),
                    "grading": submission.grading,
                    "time": submission.submission_time,
                    "status": submission.submission_status
                }
                return data, 200

        except exc.SQLAlchemyError:
            session.rollback()
            data["message"] = \
                f"An error occurred while patching submission (submission_id={submission_id})"
            return data, 500

    @authorize_submission_author
    def delete(self, submission_id: int) -> dict[str, any]:
        """Delete a submission given a submission ID

        Args:
            submission_id (int): Submission ID

        Returns:
            dict[str, any]: A message
        """

        return delete_by_id_from_model(
            Submission,
            "submission_id",
            submission_id,
            BASE_URL
        )

submissions_bp.add_url_rule("/submissions", view_func=SubmissionsEndpoint.as_view("submissions"))
submissions_bp.add_url_rule(
    "/submissions/<int:submission_id>",
    view_func=SubmissionEndpoint.as_view("submission")
)
