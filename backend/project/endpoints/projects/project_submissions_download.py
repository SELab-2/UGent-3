"""
This module contains the implementation of the endpoint that
allows teachers to download all relevant submissions for a project.
"""

from os import getenv, path, walk
from urllib.parse import urljoin
import zipfile
import io
from flask_restful import Resource
from flask import Response, stream_with_context
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from project.models.project import Project
from project.models.submission import Submission
from project.db_in import db

API_HOST = getenv("API_HOST")
UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")
BASE_URL = urljoin(f"{API_HOST}/", "/projects")

def get_last_submissions_per_user(project_id):
    """
    Get the last submissions per user for a given project
    """
    try:
        project = db.session.get(Project, project_id)
    except SQLAlchemyError:
        return {"message": "Internal server error"}, 500

    if project is None:
        return {
            "message": f"Project (project_id={project_id}) not found",
            "url": BASE_URL}, 404

    # Define a subquery to find the latest submission times for each user
    latest_submissions = db.session.query(
        Submission.uid,
        func.max(Submission.submission_time).label('max_time')
    ).filter(
        Submission.project_id == project_id,
        Submission.submission_status != 'LATE'
    ).group_by(
        Submission.uid
    ).subquery()

    # Use the subquery to fetch the actual submissions
    submissions = db.session.query(Submission).join(
        latest_submissions,
        (Submission.uid == latest_submissions.c.uid) &
        (Submission.submission_time == latest_submissions.c.max_time)
    ).all()

    return {"message": "Resource fetched succesfully", "data": submissions}, 200

class SubmissionDownload(Resource):
    """
    Resource to download all submissions for a project.
    """
    def get(self, project_id: int):
        """
        Download all submissions for a project as a zip file.
        """
        data, status_code = get_last_submissions_per_user(project_id)

        if status_code != 200:
            return data, status_code
        submissions = data["data"]

        def zip_directory_stream():
            with io.BytesIO() as memory_file:
                with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for submission in submissions:
                        submission_path = path.join(
                            UPLOAD_FOLDER,
                            str(submission.project_id),
                            "submissions",
                            str(submission.submission_id))

                        # Directory in the zip should use uid instead of submission_id
                        zip_dir_path = path.join(
                            "submissions",
                            str(submission.uid))

                        # Walk through each directory and file, maintaining the structure
                        if path.exists(submission_path) and path.isdir(submission_path):
                            for dirname, _, files in walk(submission_path):
                                arcname_dir = dirname.replace(submission_path, zip_dir_path)
                                zf.write(dirname, arcname=arcname_dir)
                                for filename in files:
                                    file_path = path.join(dirname, filename)
                                    arcname_file = file_path.replace(submission_path, zip_dir_path)
                                    zf.write(file_path, arcname=arcname_file)

                memory_file.seek(0)

                while True:
                    data = memory_file.read(4096)
                    if not data:
                        break
                    yield data

        response = Response(stream_with_context(zip_directory_stream()), mimetype='application/zip')
        response.headers['Content-Disposition'] = 'attachment; filename="submissions.zip"'
        return response
