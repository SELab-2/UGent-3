"""Endpoint for joining and leaving groups in a project"""


from os import getenv
from urllib.parse import urljoin
from dotenv import load_dotenv
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from project.utils.query_agent import insert_into_model
from project.models.group import Group
from project.models.project import Project
from project.utils.authentication import authorize_student_submission

from project import db

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(f"{API_URL}/", "groups")


class GroupStudent(Resource):
    """Api endpoint to allow students to join and leave project groups"""
    @authorize_student_submission
    def post(self, project_id, group_id, uid=None):
        """
        This function will allow students to join project groups if not full
        """
        try:
            project = db.session.query(Project).filter_by(
                project_id=project_id).first()
            if project.groups_locked:
                return {
                    "message": "Groups are locked for this project",
                    "url": RESPONSE_URL
                }, 400

            group = db.session.query(Group).filter_by(
                project_id=project_id, group_id=group_id).first()
            if group is None:
                return {
                    "message": "Group does not exist",
                    "url": RESPONSE_URL
                }, 404

            joined_groups = db.session.query(GroupStudent).filter_by(
                uid=uid, project_id=project_id).all()
            if len(joined_groups) > 0:
                return {
                    "message": "Student is already in a group",
                    "url": RESPONSE_URL
                }, 400

            joined_students = db.session.query(GroupStudent).filter_by(
                group_id=group_id, project_id=project_id).all()
            if len(joined_students) >= group.group_size:
                return {
                    "message": "Group is full",
                    "url": RESPONSE_URL
                }, 400

            req = request.json
            req["project_id"] = project_id
            req["group_id"] = group_id
            req["uid"] = uid
            return insert_into_model(
                GroupStudent,
                req,
                RESPONSE_URL,
                "group_id",
                required_fields=["project_id", "group_id", "uid"]
            )
        except SQLAlchemyError:
            data = {
            "url": urljoin(f"{API_URL}/", "projects")
            }
            data["message"] = "An error occurred while fetching the projects"
            return data, 500


    @authorize_student_submission
    def delete(self, project_id, group_id, uid=None):
        """
        This function will allow students to leave project groups
        """
        data = {
            "url": urljoin(f"{API_URL}/", "projects")
        }
        try:
            project = db.session.query(Project).filter_by(
                project_id=project_id).first()
            if project.groups_locked:
                return {
                    "message": "Groups are locked for this project",
                    "url": RESPONSE_URL
                }, 400

            group = db.session.query(Group).filter_by(
                project_id=project_id, group_id=group_id).first()
            if group is None:
                return {
                    "message": "Group does not exist",
                    "url": RESPONSE_URL
                }, 404

            if uid is None:
                return {
                    "message": "Failed to verify uid of user",
                    "url": RESPONSE_URL
                }, 400

            student_group = db.session.query(GroupStudent).filter_by(
                group_id=group_id, project_id=project_id, uid=uid).first()
            if student_group is None:
                return {
                    "message": "Student is not in the group",
                    "url": RESPONSE_URL
                }, 404

            db.session.delete(student_group)
            db.session.commit()
            data["message"] = "Student has succesfully left the group"
            return data, 200

        except SQLAlchemyError:
            data["message"] = "An error occurred while fetching the projects"
            return data, 500
