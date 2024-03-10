"""
Module that implements the /projects endpoint of the API
"""
from os import getenv
from urllib.parse import urljoin

from flask import request
from flask_restful import Resource

from project.models.projects import Project
from project.utils.query_agent import query_selected_from_model, insert_into_model
from project.utils.authentication import login_required, authorize_teacher

API_URL = getenv('API_HOST')

class ProjectsEndpoint(Resource):
    """
    Class for projects endpoints
    Inherits from flask_restful.Resource class
    for implementing get method
    """

    @login_required
    @authorize_teacher
    def get(self):
        """
        Get method for listing all available projects
        that are currently in the API
        """

        response_url = urljoin(API_URL, "projects")
        return query_selected_from_model(
            Project,
            response_url,
            select_values=["project_id", "title", "descriptions"],
            url_mapper={"project_id": response_url},
            filters=request.args
        )

    @login_required
    @authorize_teacher
    def post(self):
        """
        Post functionality for project
        using flask_restfull parse lib
        """

        return insert_into_model(
            Project,request.json,
            urljoin(API_URL, "/projects"),
            "project_id")
