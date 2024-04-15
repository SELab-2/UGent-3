"""
This file will contain the api endpoints for the /courses/<course_id>/join_codes url
"""

from os import getenv
from urllib.parse import urljoin
from dotenv import load_dotenv

from flask_restful import Resource
from flask import request
from project.utils.query_agent import query_selected_from_model, insert_into_model
from project.models.course_share_code import CourseShareCode
from project.endpoints.courses.courses_utils import get_course_abort_if_not_found
from project.utils.authentication import authorize_teacher_of_course

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(f"{API_URL}/", "courses")

class CourseJoinCodes(Resource):
    """
    This class will handle get and post queries to
    the /courses/course_id/join_codes url, only an admin of a course can do this
    """

    @authorize_teacher_of_course
    def get(self, course_id):
        """
        This function will return all the join codes of a course
        """

        get_course_abort_if_not_found(course_id)

        return query_selected_from_model(
            CourseShareCode,
            urljoin(f"{RESPONSE_URL}/", f"{str(course_id)}/", "join_codes"),
            select_values=["join_code", "expiry_time", "for_admins"],
            filters={"course_id": course_id}
        )

    @authorize_teacher_of_course
    def post(self, course_id):
        """
        Api endpoint for adding new join codes to a course, can only be done by the teacher
        """

        get_course_abort_if_not_found(course_id)

        data = request.get_json()
        data["course_id"] = course_id

        return insert_into_model(
            CourseShareCode,
            data,
            urljoin(f"{RESPONSE_URL}/", f"{str(course_id)}/", "join_codes"),
            "join_code",
            required_fields=["for_admins"]
        )
