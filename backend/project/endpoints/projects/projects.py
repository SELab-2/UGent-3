"""
Module that implements the /projects endpoint of the API
"""

import os
from urllib.parse import urljoin
import zipfile

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from flask import request, jsonify
from flask_restful import Resource

from project.db_in import db
from project.models.project import Project, Runner
from project.models.course import Course
from project.models.course_relation import CourseStudent, CourseAdmin
from project.utils.query_agent import create_model_instance
from project.utils.authentication import login_required_return_uid, authorize_teacher
from project.endpoints.projects.endpoint_parser import parse_project_params
from project.utils.models.course_utils import is_teacher_of_course
from project.utils.models.project_utils import get_course_of_project

API_URL = os.getenv('API_HOST')
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

class ProjectsEndpoint(Resource):
    """
    Class for projects endpoints
    Inherits from flask_restful.Resource class
    for implementing get method
    """

    @login_required_return_uid
    def get(self, uid=None):
        """
        Get method for listing all available projects
        that are currently in the API
        """

        data = {
            "url": urljoin(f"{API_URL}/", "projects")
        }
        try:
            # Get all the courses a user is part of
            courses = CourseStudent.query.filter_by(uid=uid).\
                with_entities(CourseStudent.course_id).all()
            courses += CourseAdmin.query.filter_by(uid=uid).\
                with_entities(CourseAdmin.course_id).all()
            courses += Course.query.filter_by(teacher=uid).with_entities(Course.course_id).all()
            courses = [c[0] for c in courses] # Remove the tuple wrapping the course_id

            # Filter the projects based on the query parameters
            filters = dict(request.args)
            conditions = []
            for key, value in filters.items():
                if key in Project.__table__.columns:
                    conditions.append(getattr(Project, key) == value)

            # Get the projects
            projects = Project.query
            projects = projects.filter(and_(*conditions)) if conditions else projects
            projects = projects.all()
            projects = [p for p in projects if get_course_of_project(p.project_id) in courses]

            # Return the projects
            data["message"] = "Successfully fetched the projects"
            data["data"] = [{
                "project_id": urljoin(f"{API_URL}/", f"projects/{p.project_id}"),
                "title": p.title,
                "course_id": urljoin(f"{API_URL}/", f"courses/{p.course_id}")
            } for p in projects]
            return data

        except SQLAlchemyError:
            data["message"] = "An error occurred while fetching the projects"
            return data, 500

    @authorize_teacher
    def post(self, teacher_id=None):
        """
        Post functionality for project
        using flask_restfull parse lib
        """
        project_json = parse_project_params()

        if not is_teacher_of_course(teacher_id, project_json["course_id"]):
            return {"message":"You are not the teacher of this course"}, 403

        filename = None
        if "assignment_file" in request.files:
            file = request.files["assignment_file"]
            filename = os.path.basename(file.filename)

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
                file_path = os.path.join(project_upload_directory, filename)
                file.save(file_path)
                with zipfile.ZipFile(file_path) as upload_zip:
                    upload_zip.extractall(project_upload_directory)

                if not new_project.runner and \
                    os.path.exists(os.path.join(project_upload_directory, "Dockerfile")):

                    new_project.runner = Runner.CUSTOM
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
