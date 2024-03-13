"""
Module for getting the assignment files
of a project
"""
import os
from urllib.parse import urljoin

from flask import send_from_directory
from werkzeug.utils import safe_join

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
        directory = safe_join(os.getcwd(), file_url)

        return send_from_directory(directory, project.assignment_file, as_attachment=True)
