"""
This file contains the endpoint to join a course using a join code
"""


from os import getenv
from datetime import datetime

from flask import request
from flask_restful import Resource

from sqlalchemy.exc import SQLAlchemyError

from project.models.course_share_code import CourseShareCode
from project.models.course_relation import CourseStudent, CourseAdmin
from project.utils.misc import is_valid_uuid
from project.db_in import db
from project.utils.authentication import login_required_return_uid

API_URL = getenv("API_HOST")

class CourseJoin(Resource):
    """
    Class that will respond to the /courses/join link
    students or admins with a join code can join a course
    """

    @login_required_return_uid
    def post(self, uid=None): # pylint: disable=too-many-return-statements
        """
        Post function for /courses/join
        students or admins with a join code can join a course
        """

        response = {
            "url": f"{API_URL}/courses/join"
        }

        data = request.get_json()
        if not "join_code" in data:
            return {"message": "join_code is required"}, 400

        join_code = data["join_code"]

        if not is_valid_uuid(join_code):
            response["message"] = "Invalid join code"
            return response, 400

        share_code = CourseShareCode.query.filter_by(join_code=join_code).first()

        if not share_code:
            response["message"] = "Invalid join code"
            return response, 400

        if share_code.expiry_time and share_code.expiry_time < datetime.now().date():
            response["message"] = "Join code has expired"
            return response, 400


        course_id = share_code.course_id
        is_for_admins = share_code.for_admins

        course_relation = CourseStudent
        if is_for_admins:
            course_relation = CourseAdmin

        try:
            relation = course_relation.query.filter_by(course_id=course_id, uid=uid).first()
            if relation:
                response["message"] = "User already in course"
                response["data"] = {
                    "course_id": course_id
                }
                return response, 409
        except SQLAlchemyError:
            response["message"] = "Internal server error"
            return response, 500

        course_relation = course_relation(course_id=course_id, uid=uid)

        try:
            db.session.add(course_relation)
            db.session.commit()
            response["data"] = {
                "course_id": course_id
            }
            response["message"] = "User added to course"
            return response, 201
        except SQLAlchemyError:
            db.session.rollback()
            response["message"] = "Internal server error"
            return response, 500
