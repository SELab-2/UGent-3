"""
This module contains the API endpoint for the submissions
"""

from os import path, makedirs, getenv
from urllib.parse import urljoin
from datetime import datetime
from zoneinfo import ZoneInfo
from shutil import rmtree
from flask import request
from flask_restful import Resource
from sqlalchemy import exc
from project.executor import executor
from project.db_in import db
from project.models.submission import Submission, SubmissionStatus
from project.models.project import Project
from project.models.user import User
from project.utils.files import all_files_uploaded
from project.utils.user import is_valid_user
from project.utils.project import is_valid_project
from project.utils.query_agent import query_selected_from_model
from project.utils.authentication import authorize_student_submission, authorize_submissions_request
from project.utils.submissions.evaluator import run_evaluator

API_HOST = getenv("API_HOST")
UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")
BASE_URL =  urljoin(f"{API_HOST}/", "/submissions")
TIMEZONE = getenv("TIMEZONE", "GMT")

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
                valid, message = is_valid_user(session, request.form.get("uid"))
                if not valid:
                    data["message"] = message
                    return data, 400
                submission.uid = request.form.get("uid")

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
                is_late = deadlines is not None
                if deadlines:
                    for deadline in deadlines:
                        if submission.submission_time < deadline.deadline:
                            is_late = False

                if project.runner:
                    submission.submission_status = SubmissionStatus.RUNNING
                else:
                    submission.submission_status = SubmissionStatus.LATE if is_late \
                        else SubmissionStatus.SUCCESS

                # Submission_id needed for the file location
                session.add(submission)
                session.commit()

                # Save the files
                submission.submission_path = path.join(UPLOAD_FOLDER, str(submission.project_id),
                    "submissions", str(submission.submission_id))
                try:
                    makedirs(submission.submission_path, exist_ok=True)
                    input_folder = path.join(submission.submission_path, "submission")
                    makedirs(input_folder, exist_ok=True)
                    for file in files:
                        file.save(path.join(input_folder, file.filename))
                except OSError:
                    rmtree(submission.submission_path)
                    session.rollback()

                if project.runner:
                    submission.submission_status = SubmissionStatus.RUNNING
                    executor.submit(
                        run_evaluator,
                        submission,
                        path.join(UPLOAD_FOLDER, str(project.project_id)),
                        project.runner.value,
                        False)

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
                return data, 202

        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            data["message"] = "An error occurred while creating a new submission"
            return data, 500
