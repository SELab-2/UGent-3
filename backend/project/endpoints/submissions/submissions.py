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
from sqlalchemy import exc, and_
from project.executor import executor
from project.db_in import db
from project.models.submission import Submission, SubmissionStatus
from project.models.project import Project
from project.models.course import Course
from project.models.course_relation import CourseAdmin
from project.utils.files import all_files_uploaded
from project.utils.project import is_valid_project
from project.utils.authentication import authorize_student_submission, login_required_return_uid
from project.utils.submissions.evaluator import run_evaluator
from project.utils.models.project_utils import get_course_of_project
from project.utils.models.submission_utils import submission_response

API_HOST = getenv("API_HOST")
UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")
BASE_URL =  urljoin(f"{API_HOST}/", "/submissions")
TIMEZONE = getenv("TIMEZONE", "GMT")

class SubmissionsEndpoint(Resource):
    """API endpoint for the submissions"""

    @login_required_return_uid
    def get(self, uid=None) -> dict[str, any]:
        """Get all the submissions from a user

        Returns:
            dict[str, any]: The list of submission URLs
        """

        data = {
            "url": BASE_URL
        }
        filters = dict(request.args)
        print(filters)
        try:
            # Check the uid query parameter
            user_id = filters.get("uid")
            if user_id and not isinstance(user_id, str):
                data["message"] = f"Invalid user (uid={user_id})"
                return data, 400

            # Check the project_id query parameter
            project_id = filters.get("project_id")
            if project_id:
                if not project_id.isdigit():
                    data["message"] = f"Invalid project (project_id={project_id})"
                    return data, 400
                filters["project_id"] = int(project_id)

            if set(filters.keys()) - {"grading", "submission_id", "uid", "project_id", "submission_time"}:
                data["message"] = "Invalid data field given."
                return data, 400

            # Get the courses
            courses = Course.query.filter_by(teacher=uid).\
                with_entities(Course.course_id).all()
            courses += CourseAdmin.query.filter_by(uid=uid).\
                with_entities(CourseAdmin.course_id).all()
            courses = [c[0] for c in courses] # Remove the tuple wrapping the course_id

            # Filter the courses based on the query parameters
            conditions = []
            for key, value in filters.items():
                if key in Submission.__table__.columns:
                    conditions.append(getattr(Submission, key) == value)

            # Get the submissions
            submissions = Submission.query
            submissions = submissions.filter(and_(*conditions)) if conditions else submissions
            submissions = submissions.all()
            submissions = [
                s for s in submissions if
                s.uid == uid or get_course_of_project(s.project_id) in courses
            ]

            # Return the submissions
            data["message"] = "Successfully fetched the submissions"
            data["data"] = [{
                "submission_id": urljoin(f"{API_HOST}/", f"/submissions/{s.submission_id}"),
                "uid": urljoin(f"{API_HOST}/", f"users/{s.uid}"),
                "project_id": urljoin(f"{API_HOST}/", f"projects/{s.project_id}"),
                "grading": s.grading,
                "submission_time": s.submission_time,
                "submission_status": s.submission_status
            } for s in submissions]
            return data

        except exc.SQLAlchemyError:
            data["message"] = "An error occurred while fetching the submissions"
            return data, 500

    @authorize_student_submission
    def post(self, uid=None) -> dict[str, any]:
        """Post a new submission to a project

        Returns:
            dict[str, any]: The URL to the submission
        """

        data = {
            "url": BASE_URL
        }
        try:
            if set(request.form.keys()) - {"project_id", "files"}:
                data["message"] = "Invalid data fields, only 'project_id' and 'files' are allowed"
                return data, 400

            with db.session() as session:
                submission = Submission()

                # User
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
                data["data"] = submission_response(submission, API_HOST)
                return data, 201

        except exc.SQLAlchemyError:
            session.rollback()
            data["message"] = "An error occurred while creating a new submission"
            return data, 500
