"""
Module that implements the /projects endpoint of the API
"""
import os
from urllib.parse import urljoin
import zipfile

from flask import request
from flask_restful import Resource

from project.models.project import Project
from project.utils.query_agent import query_selected_from_model, create_model_instance

from project.endpoints.projects.endpoint_parser import parse_project_params

API_URL = os.getenv('API_HOST')
UPLOAD_FOLDER = os.getenv('UPLOAD_URL')

class ProjectsEndpoint(Resource):
    """
    Class for projects endpoints
    Inherits from flask_restful.Resource class
    for implementing get method
    """

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

    def post(self):
        """
        Post functionality for project
        using flask_restfull parse lib
        """

        file = request.files["assignment_file"]
        project_json = parse_project_params()
        filename = file.filename.split("/")[-1]

        # save the file that is given with the request

        new_project = create_model_instance(
            Project,
            project_json,
            urljoin(f"{API_URL}/", "/projects"),
            required_fields=[
                "title",
                "descriptions",
                "course_id",
                "visible_for_students",
                "archieved"]
        )

        project_upload_directory = f"{UPLOAD_FOLDER}{new_project.project_id}"

        file_location = "." + os.path.join(project_upload_directory)

        if not os.path.exists(project_upload_directory):
            os.makedirs(file_location, exist_ok=True)

        file.save(file_location + "/" + filename)
        try:
            with zipfile.ZipFile(file_location + "/" + filename) as upload_zip:
                upload_zip.extractall(file_location)
        except zipfile.BadZipfile:
            return {"message": "Please provide a .zip file for uploading the instructions"}, 400

        return {
            "message": "Project created succesfully",
            "data": new_project,
            "url": f"{API_URL}/projects/{new_project.project_id}"
        }, 201
