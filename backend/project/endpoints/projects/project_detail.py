"""
Module for project details page
for example /projects/1 if the project id of
the corresponding project is 1
"""
from os import getenv
from urllib.parse import urljoin

from flask import request
from flask_restful import Resource

from project.models.projects import Project
from project.utils.query_agent import query_by_id_from_model, delete_by_id_from_model, \
    patch_by_id_from_model


API_URL = getenv('API_HOST')
RESPONSE_URL = urljoin(API_URL, "projects")

class ProjectDetail(Resource):
    """
    Class for projects/id endpoints
    Inherits from flask_restful.Resource class
    for implementing get, delete and put methods
    """

    def get(self, project_id):
        """
        Get method for listing a specific project
        filtered by id of that specific project
        the id fetched from the url with the reaparse
        """

        return query_by_id_from_model(
            Project,
            "project_id",
            project_id,
            RESPONSE_URL)

    def patch(self, project_id):
        """
        Update method for updating a specific project
        filtered by id of that specific project
        """

        return patch_by_id_from_model(
            Project,
            "project_id",
            project_id,
            RESPONSE_URL,
            request.json
        )

    def delete(self, project_id):
        """
        Delete a project and all of its submissions in cascade
        done by project id
        """

        return delete_by_id_from_model(
            Project,
            "project_id",
            project_id,
            RESPONSE_URL)
