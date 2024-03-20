"""
This file will contain the api endpoints for the /courses/<course_id>/join_codes url
"""

from os import getenv
from urllib.parse import urljoin
from dotenv import load_dotenv

from flask_restful import Resource
from project.utils.query_agent import query_by_id_from_model, delete_by_id_from_model
from project.models.course_share_code import CourseShareCode
from project.endpoints.courses.join_codes.join_codes_utils import check_course_exists
from project.utils.authentication import authorize_teacher_of_course

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(f"{API_URL}/", "courses")

class CourseJoinCode(Resource):
    """
    This class will handle post and delete queries to
    the /courses/course_id/join_codes/<join_code> url, only an admin of a course can do this
    """

    @check_course_exists
    def get(self, course_id, join_code):
        """
        This function will return all the join codes of a course
        """

        return query_by_id_from_model(
            CourseShareCode,
            "join_code",
            join_code,
            urljoin(f"{RESPONSE_URL}/", f"{str(course_id)}/", "join_codes")
        )

    @check_course_exists
    @authorize_teacher_of_course
    def delete(self, course_id, join_code):
        """
        Api endpoint for deleting join codes from a course, can only be done by the teacher
        """

        return delete_by_id_from_model(
            CourseShareCode,
            "join_code",
            join_code,
            urljoin(f"{RESPONSE_URL}/", f"{str(course_id)}/", "join_codes")
        )
