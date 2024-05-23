"""This module contains helper functions related to projects for accessing the database"""

from os import getenv

from dotenv import load_dotenv

from flask import abort, make_response
from sqlalchemy.exc import SQLAlchemyError

from project import db
from project.models.project import Project

load_dotenv()
API_URL = getenv("API_HOST")

def get_project(project_id):
    """Returns the project associated with project_id or the appropriate error"""
    if isinstance(project_id, str) and not project_id.isnumeric():
        abort(make_response(({"message": f"{project_id} is not a valid project id"}
                             , 400)))
    try:
        project = db.session.get(Project, project_id)
    except SQLAlchemyError:
        db.session.rollback()
        abort(make_response(({"message": "An error occurred while fetching the project"}
                             , 500)))

    if not project:
        abort(make_response(({"message":f"Project with id: {project_id} not found"}, 404)))

    return project

def get_course_of_project(project_id):
    """This function returns the course_id of the course associated with the project: project_id"""
    project = get_project(project_id)
    return project.course_id

def project_visible(project_id):
    """Determine whether a project is visible for students"""
    project = get_project(project_id)
    return project.visible_for_students
