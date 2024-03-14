"""
Module for getting the assignment files
of a project
"""
import os
from urllib.parse import urljoin

from flask import send_from_directory
from werkzeug.utils import safe_join
from sqlalchemy.exc import SQLAlchemyError

from flask_restful import Resource

from project.models.project import Project

API_URL = os.getenv('API_HOST')
RESPONSE_URL = urljoin(API_URL, "projects")
UPLOAD_FOLDER = os.getenv('UPLOAD_URL')

class ProjectAssignmentFiles(Resource):
    """
    Class for getting the assignment files of a project
    """
    def get(self, project_id):
        """
        Get the assignment files of a project
        """
        try:
            project = Project.query.filter(getattr(Project, "project_id") == project_id).first()
            if project is None:
                return {
                    "message": "Project not found",
                    "url": RESPONSE_URL,
                }, 404
        except SQLAlchemyError:
            return {
                "message": "Something went wrong querying the project",
                "url": RESPONSE_URL
            }, 500

        file_url = safe_join(UPLOAD_FOLDER, f"{project_id}")

        if not os.path.isfile(file_url):
            # no file is found so return 404
            return {
                "message": "No assignment file found for this project",
                "url": file_url
            }, 404

        return send_from_directory(file_url,project.assignment_file)
