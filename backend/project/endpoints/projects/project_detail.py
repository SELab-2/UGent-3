"""
Module for project details page
for example /projects/1 if the project id of
the corresponding project is 1
"""
import os
import zipfile
from urllib.parse import urljoin

from flask import request
from flask_restful import Resource

from project.db_in import db

from project.models.project import Project
from project.utils.query_agent import query_by_id_from_model, delete_by_id_from_model, \
    patch_by_id_from_model
from project.utils.authentication import authorize_teacher_or_project_admin, \
    authorize_teacher_of_project, authorize_project_visible

from project.endpoints.projects.endpoint_parser import parse_project_params

API_URL = os.getenv('API_HOST')
RESPONSE_URL = urljoin(API_URL, "projects")
UPLOAD_FOLDER = os.getenv('UPLOAD_URL')


class ProjectDetail(Resource):
    """
    Class for projects/id endpoints
    Inherits from flask_restful.Resource class
    for implementing get, delete and put methods
    """

    @authorize_project_visible
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

    @authorize_teacher_or_project_admin
    def patch(self, project_id):
        """
        Update method for updating a specific project
        filtered by id of that specific project
        """
        project_json = parse_project_params()

        output, status_code = patch_by_id_from_model(
            Project,
            "project_id",
            project_id,
            RESPONSE_URL,
            project_json
        )
        if status_code != 200:
            return output, status_code

        if "assignment_file" in request.files:
            file = request.files["assignment_file"]
            filename = os.path.basename(file.filename)
            project_upload_directory = os.path.join(f"{UPLOAD_FOLDER}", f"{project_id}")
            os.makedirs(project_upload_directory, exist_ok=True)
            try:
                # remove the old file
                try:
                    to_rem_files = os.listdir(project_upload_directory)
                    for to_rem_file in to_rem_files:
                        to_rem_file_path = os.path.join(project_upload_directory, to_rem_file)
                        if os.path.isfile(to_rem_file_path):
                            os.remove(to_rem_file_path)
                except FileNotFoundError:
                    db.session.rollback()
                    return ({
                        "message": "Something went wrong deleting the old project files",
                        "url": f"{API_URL}/projects/{project_id}"
                    })

                # removed all files now upload the new files
                file.save(os.path.join(project_upload_directory, filename))
                zip_location = os.path.join(project_upload_directory, filename)
                with zipfile.ZipFile(zip_location) as upload_zip:
                    upload_zip.extractall(project_upload_directory)

            except zipfile.BadZipfile:
                db.session.rollback()
                return ({
                            "message":
                                "Please provide a valid .zip file for updating the instructions",
                            "url": f"{API_URL}/projects/{project_id}"
                        },
                        400)

        return output, status_code

    @authorize_teacher_of_project
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
