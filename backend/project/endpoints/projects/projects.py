"""
Module that implements the /projects endpoint of the API
"""
import os
from urllib.parse import urljoin
import zipfile
from sqlalchemy.exc import SQLAlchemyError

from flask import request, jsonify
from flask_restful import Resource

from project.db_in import db

from project.models.project import Project
from project.utils.query_agent import query_selected_from_model, create_model_instance
from project.utils.authentication import authorize_teacher

from project.endpoints.projects.endpoint_parser import parse_project_params

API_URL = os.getenv('API_HOST')
UPLOAD_FOLDER = os.getenv('UPLOAD_URL')


class ProjectsEndpoint(Resource):
    """
    Class for projects endpoints
    Inherits from flask_restful.Resource class
    for implementing get method
    """

    @authorize_teacher
    def get(self, teacher_id=None):
        """
        Get method for listing all available projects
        that are currently in the API
        """
        response_url = urljoin(API_URL, "projects")
        return query_selected_from_model(
            Project,
            response_url,
            select_values=["project_id", "title", "description"],
            url_mapper={"project_id": response_url},
            filters=request.args
        )

    @authorize_teacher
    def post(self, teacher_id=None):
        """
        Post functionality for project
        using flask_restfull parse lib
        """

        project_json = parse_project_params()
        filename = None
        if "assignment_file" in request.files:
            file = request.files["assignment_file"]
            filename = os.path.basename(file.filename)
            project_json["assignment_file"] = filename

        # save the file that is given with the request
        try:
            new_project, status_code = create_model_instance(
                Project,
                project_json,
                urljoin(f"{API_URL}/", "/projects"),
                required_fields=[
                    "title",
                    "description",
                    "course_id",
                    "visible_for_students",
                    "archived"]
            )
        except SQLAlchemyError:
            return jsonify({"error": "Something went wrong while inserting into the database.",
                            "url": f"{API_URL}/projects"}), 500

        if status_code == 400:
            return new_project, status_code

        project_upload_directory = os.path.join(f"{UPLOAD_FOLDER}", f"{new_project.project_id}")
        os.makedirs(project_upload_directory, exist_ok=True)
        if filename is not None:
            try:
                file.save(os.path.join(project_upload_directory, filename))
                zip_location = os.path.join(project_upload_directory, filename)
                with zipfile.ZipFile(zip_location) as upload_zip:
                    upload_zip.extractall(project_upload_directory)
            except zipfile.BadZipfile:
                os.remove(os.path.join(project_upload_directory, filename))
                db.session.rollback()
                return ({
                            "message": "Please provide a .zip file for uploading the instructions",
                            "url": f"{API_URL}/projects"
                        },
                        400)
        return {
            "message": "Project created succesfully",
            "data": new_project,
            "url": f"{API_URL}/projects/{new_project.project_id}"
        }, 201
