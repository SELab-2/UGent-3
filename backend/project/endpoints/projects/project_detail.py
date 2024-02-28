"""
Module for project details page
for example /projects/1 if the project id of
the corresponding project is 1
"""

from flask import jsonify
from flask_restful import Resource, abort
from sqlalchemy import exc
from project.endpoints.projects.endpoint_parser import parse_project_params

from project import db
from project.models.projects import Projects


class ProjectDetail(Resource):
    """
    Class for projects/id endpoints
    Inherits from flask_restful.Resource class
    for implementing get, delete and put methods
    """

    def abort_if_not_present(self, project):
        """
        Check if the project exists in the database
        and if not abort the request and give back a 404 not found
        """
        if project is None:
            abort(404)

    def get(self, project_id):
        """
        Get method for listing a specific project
        filtered by id of that specific project
        the id fetched from the url with the reaparse
        """

        # fetch the project with the id that is specified in the url
        project = Projects.query.filter_by(project_id=project_id).first()

        self.abort_if_not_present(project)

        # return the fetched project and return 200 OK status
        return jsonify(project)

    def patch(self, project_id):
        """
        Update method for updating a specific project
        filtered by id of that specific project
        """

        # get the project that need to be edited
        project = Projects.query.filter_by(project_id=project_id).first()  # .update(values=values)

        # check which values are not None is the dict
        # if it is not None is needs to be modified in the database

        # commit the changes and return the 200 OK code if it succeeds, else 500
        try:
            var_dict = parse_project_params()
            for key, value in var_dict.items():
                setattr(project, key, value)
            db.session.commit()
            # get the updated version
            return {"message": f"Succesfully changed project with id: {project.project_id}"}, 200
        except exc.SQLAlchemyError:
            db.session.rollback()
            return ({"message":
                        f"Something unexpected happenend when trying to edit project {id}"},
                    500)

    def delete(self, project_id):
        """
        Detele a project and all of its submissions in cascade
        done by project id
        """

        # fetch the project that needs to be removed
        deleted_project = Projects.query.filter_by(project_id=project_id).first()

        # check if its an existing one
        self.abort_if_not_present(deleted_project)

        # if it exists delete it and commit the changes in the database
        try:
            db.session.delete(deleted_project)
            db.session.commit()

            # return 200 if content is deleted succesfully
            return {"message": f"Project with id:{project_id} deleted successfully!"}, 200
        except exc.SQLAlchemyError:
            return ({"message":
                        f"Something unexpected happened when removing project {project_id}"},
                    500)
