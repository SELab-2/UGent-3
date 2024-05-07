"""Endpoint for creating/deleting groups in a project"""
from os import getenv
from urllib.parse import urljoin
from dotenv import load_dotenv
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from project.models.project import Project
from project.models.course import Course
from project.models.group import Group
from project.utils.query_agent import query_selected_from_model, insert_into_model
from project.utils.authentication import login_required, authorize_teacher
from project import db

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(f"{API_URL}/", "groups")


class Groups(Resource):
    """Api endpoint for the /project/project_id/groups link"""

    @login_required
    def get(self, project_id):
        """
        Get function for /project/project_id/groups this will be the main endpoint
        to get all groups for a project
        """
        return query_selected_from_model(
            Group,
            RESPONSE_URL,
            url_mapper={"group_id": RESPONSE_URL},
            filters={"project_id": project_id}
        )

    @authorize_teacher
    def post(self, project_id, teacher_id=None):
        """
        This function will create a new group for a project
        if the body of the post contains a group_size and project_id exists
        """

        req = request.json
        req["project_id"] = project_id
        return insert_into_model(
            Group,
            req,
            RESPONSE_URL,
            "group_id",
            required_fields=["project_id", "group_size"]
        )

    @authorize_teacher
    def delete(self, project_id, teacher_id=None):
        """
        This function will delete a group
        if group_id is provided and request is from teacher
        """

        req = request.json
        print(req)
        group_id = req.get("group_id")

        if group_id is None:
            return {
                "message": "Bad request: group_id is required",
                "url": RESPONSE_URL
            }, 400

        try:
            project = db.session.query(Project).filter_by(
                project_id=project_id).first()
            if project is None:
                return {
                    "message": "Project associated with group does not exist",
                    "url": RESPONSE_URL
                }, 404
            course = db.session.query(Course).filter_by(
                course_id=project.course_id).first()
            if course is None:
                return {
                    "message": "Course associated with project does not exist",
                    "url": RESPONSE_URL
                }, 404
            if course.teacher != teacher_id:
                return {
                    "message": "Unauthorized",
                    "url": RESPONSE_URL
                }, 401
            group = db.session.query(Group).filter_by(
                project_id=project_id, group_id=group_id).first()
            db.session.delete(group)
            db.session.commit()
            return {
                "message": "Group deleted",
                "url": RESPONSE_URL
            }, 204
        except SQLAlchemyError:
            return {
                "message": "Database error",
                "url": RESPONSE_URL
            }, 500
