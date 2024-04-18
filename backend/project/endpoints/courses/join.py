"""
This file contains the endpoint to join a course using a join code
"""


from os import getenv
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import request
from flask_restful import Resource

from sqlalchemy.exc import SQLAlchemyError

from project.models.course_share_code import CourseShareCode
from project.models.course_relation import CourseStudent, CourseAdmin


TIMEZONE = getenv("TIMEZONE", "GMT")
API_URL = getenv("API_HOST")

class CourseJoin(Resource):
    """
    Class that will respond to the /courses/course_id/students link
    teachers should be able to assign and remove students from courses,
    and everyone should be able to list all students assigned to a course
    """

    def post(self, uid=None): # pylint: disable=too-many-return-statements
        """
        Post function at /courses/course_id/students
        to assign a student to a course
        only teachers and admins can do this
        """

        response = {
            "url": f"{API_URL}/courses/join"
        }

        data = request.get_json()
        if not "join_code" in data:
            return {"message": "join_code is required"}, 400

        join_code = data["join_code"]
        share_code = CourseShareCode.query.filter_by(join_code=join_code).first()

        if not share_code:
            response["message"] = "Invalid join code"
            return response, 400

        if share_code.expiry_time and share_code.expiry_time < datetime.now(ZoneInfo(TIMEZONE)):
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
                return response, 400
        except SQLAlchemyError:
            response["message"] = "Internal server error"
            return response, 500

        course_relation = course_relation(course_id=course_id, uid=uid)

        try:
            course_relation.insert()
            response["message"] = "User added to course"
            return response, 201
        except SQLAlchemyError:
            response["message"] = "Internal server error"
            return response, 500
