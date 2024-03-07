"""
Module that implements the /projects endpoint of the API
"""
import os
from os import getenv
from urllib.parse import urljoin

from flask import request
from flask_restful import Resource

from project.models.projects import Project
from project.utils.query_agent import query_selected_from_model, insert_into_model

API_URL = getenv('API_HOST')
UPLOAD_FOLDER = getenv('UPLOAD_URL')
ALLOWED_EXTENSIONS = {'zip'}

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

        # save the file that is given with the request
        if allowed_file(file.filename):
            file.save("."+os.path.join(UPLOAD_FOLDER, file.filename))
        else:
            print("no zip file given")
        # return insert_into_model(Project, request.json, urljoin(API_URL, "/projects"))
        print(request.form)
        project_json = {}
        for key, value in request.form.items():
            print("key: {}, value: {}".format(key, value))
            project_json[key] = value
        print(project_json)
        new_project = insert_into_model(Project, project_json, urljoin(API_URL, "/projects"))
        print(new_project)

        return new_project
