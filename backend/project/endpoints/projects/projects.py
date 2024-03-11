"""
Module that implements the /projects endpoint of the API
"""
import os
from os import getenv
from urllib.parse import urljoin

from flask import request
from flask_restful import Resource

import zipfile

from project.models.projects import Project
from project.utils.query_agent import query_selected_from_model, insert_into_model, create_model_instance

from project.endpoints.projects.endpoint_parser import parse_project_params

API_URL = getenv('API_HOST')
UPLOAD_FOLDER = getenv('UPLOAD_URL')
ALLOWED_EXTENSIONS = {'zip'}

def parse_immutabledict(request):
    output_json = {}
    for key, value in request.form.items():
        if value == "false":
            print("false")
            output_json[key] = False
        if value == "true":
            output_json[key] = True
        else:
            output_json[key] = value
    return output_json

def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

        # save the file that is given with the request

        new_new_project = create_model_instance(
            Project,
            project_json,
            urljoin(API_URL, "/projects"),
            required_fields=["title", "descriptions", "course_id", "visible_for_students", "archieved"]
        )

        print(new_new_project)
        id = new_new_project.project_id
        print(id)
        project_upload_directory = f"{UPLOAD_FOLDER}{new_new_project.project_id}"
        file_location = "."+os.path.join(project_upload_directory)
        print(file_location)
        # print(new_new_project.json)
        if not os.path.exists(project_upload_directory):
            os.makedirs(file_location)

        if allowed_file(file.filename):
            file.save(file_location+"/"+file.filename)
            with zipfile.ZipFile(file_location+"/"+file.filename) as zip:
                zip.extractall(file_location)
        else:
            return {"message": "Please provide a .zip file for uploading the instructions"}, 400

        return {
            "message": "Project created succesfully",
            "data": new_new_project,
            "url": f"{API_URL}/projects/{id}"
        }, 200
