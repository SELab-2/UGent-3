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
from project.utils.query_agent import query_by_id_from_model

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
        json, status_code = query_by_id_from_model(
            Project,
            "project_id",
            project_id,
            "RESPONSE_URL"
        )

        if status_code != 200:
            return json, status_code

        project = json["data"]
        file_url = safe_join(UPLOAD_FOLDER, str(project_id))

        if not os.path.isfile(safe_join(file_url, project.assignment_file)):
            # no file is found so return 404
            return {
                "message": "No assignment file found for this project",
                "url": file_url
            }, 404

        return send_from_directory(file_url, project.assignment_file)
