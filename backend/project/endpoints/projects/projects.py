"""
Module that implements the /projects endpoint of the API
"""

from flask import jsonify
from flask_restful import Resource
from sqlalchemy import exc

from project import db
from project.models.projects import Projects
from project.endpoints.projects.endpoint_parser import parse_project_params


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
        projects = Projects.query.all()

        # return all valid entries for a project and return a 200 OK code
        return jsonify(projects)

    def post(self):
        """
        Post functionality for project
        using flask_restfull parse lib
        """
        args = parse_project_params()

        # create a new project object to add in the API later
        new_project = Projects(
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
            return jsonify(new_project), 201
        except exc.SQLAlchemyError:
            return ({"message":
                        "Something unexpected happenend when trying to add a new project"},
                    500)
