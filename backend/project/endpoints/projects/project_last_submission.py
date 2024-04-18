"""
This module gives the last submission for a project for every user
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

class SubmissionPerUser(Resource):
    """
    Recourse to get all the submissions for users
    """

    def get(self, project_id: int):
        """
        Download all submissions for a project as a zip file.
        """

        try:
            project = Project.query.get(project_id)
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

        if not submissions:
            return {"message": "No submissions found", "url": BASE_URL}, 404

        return {"message": "Resource fetched succesfully", "data": submissions}, 200
