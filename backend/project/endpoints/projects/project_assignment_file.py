"""
Module for getting the assignment files
of a project
"""
import os
from urllib.parse import urljoin

from flask import send_from_directory, request

from flask_restful import Resource

from project.utils.authentication import authorize_project_visible

API_URL = os.getenv('API_HOST')
RESPONSE_URL = urljoin(API_URL, "projects")
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')

ASSIGNMENT_FILE_NAME = "assignment.md"

class ProjectAssignmentFiles(Resource):
    """
    Class for getting the assignment files of a project
    """

    @authorize_project_visible
    def get(self, project_id):
        """
        Get the assignment files of a project
        """

        language = request.args.get('lang')
        directory_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, str(project_id)))
        file_name = ASSIGNMENT_FILE_NAME
        if language:
            potential_file = f"assignment_{language}.md"
            if os.path.isfile(os.path.join(directory_path, potential_file)):
                file_name = potential_file
            else:
                # Find any .md file that starts with "assignment"
                for filename in os.listdir(directory_path):
                    if filename.startswith("assignment") and filename.endswith(".md"):
                        file_name = filename
                        break


        assignment_file = os.path.join(directory_path, file_name)

        if not os.path.isfile(assignment_file):
            # no file is found so return 404
            return {
                "message": "No assignment file found for this project",
                "url": f"{API_URL}/projects/{project_id}/assignment"
            }, 404



        return send_from_directory(directory_path, ASSIGNMENT_FILE_NAME)
