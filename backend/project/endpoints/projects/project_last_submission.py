"""
This module gives the last submission for a project for every user
"""

from os import getenv
from urllib.parse import urljoin
from flask_restful import Resource
from project.endpoints.projects.project_submissions_download import get_last_submissions_per_user
from project.utils.authentication import authorize_teacher_or_project_admin

API_HOST = getenv("API_HOST")
UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")
BASE_URL = urljoin(f"{API_HOST}/", "/projects")

class SubmissionPerUser(Resource):
    """
    Recourse to get all the submissions for users
    """

    @authorize_teacher_or_project_admin
    def get(self, project_id: int):
        """
        Download all submissions for a project as a zip file.
        """

        return get_last_submissions_per_user(project_id)
