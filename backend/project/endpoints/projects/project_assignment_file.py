"""
Module for getting the assignment files
of a project
"""
import os
from urllib.parse import urljoin

from flask import jsonify, send_from_directory, send_file
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

        project = Project.query.filter(getattr(Project, "project_id") == project_id).first()

        file_url = safe_join(f"{UPLOAD_FOLDER}", f"{project_id}")

        directory = safe_join(os.getcwd(), file_url)

        return send_from_directory(directory, project.assignment_file, as_attachment=True)