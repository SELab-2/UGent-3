"""
Module that implements the /projects endpoint of the API
"""
from os import getenv
from dotenv import load_dotenv

from flask import jsonify
from flask_restful import Resource
from sqlalchemy import exc


from project import db
from project.models.projects import Project
from project.endpoints.projects.endpoint_parser import parse_project_params

load_dotenv()
API_URL = getenv('API_HOST')

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
        try:
            projects = Project.query.with_entities(
                Project.project_id,
                Project.title,
                Project.descriptions
            ).all()

            results = [{
                "project_id": row[0],
                "title": row[1],
                "descriptions": row[2]
            } for row in projects]

            # return all valid entries for a project and return a 200 OK code
            return {
                "data": results,
                "url": f"{API_URL}/projects",
                "message": "Projects fetched successfully"
            }, 200
        except exc.SQLAlchemyError:
            return {
                "message": "Something unexpected happenend when trying to get the projects",
                "url": f"{API_URL}/projects"
            }, 500

    def post(self):
        """
        Post functionality for project
        using flask_restfull parse lib
        """
        args = parse_project_params()

        # create a new project object to add in the API later
        new_project = Project(
            title=args['title'],
            descriptions=args['descriptions'],
            assignment_file=args['assignment_file'],
            deadline=args['deadline'],
            course_id=args['course_id'],
            visible_for_students=args['visible_for_students'],
            archieved=args['archieved'],
            test_path=args['test_path'],
            script_name=args['script_name'],
            regex_expressions=args['regex_expressions']
        )

        # add the new project to the database and commit the changes

        try:
            db.session.add(new_project)
            db.session.commit()
            new_project_json = jsonify(new_project).json

            return {
                "url": f"{API_URL}/projects/{new_project_json['project_id']}",
                "message": "Project posted successfully",
                "data": new_project_json
            }, 201
        except exc.SQLAlchemyError:
            return ({
                "url": f"{API_URL}/projects",
                "message": "Something unexpected happenend when trying to add a new project",
                "data": jsonify(new_project).json
            }, 500)
