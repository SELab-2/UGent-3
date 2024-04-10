"""
This file contains the main endpoint for the /courses url.
This endpoint is used to get all courses and filter by given
query parameter like /courses?parameter=...
parameters can be either one of the following: teacher,ufora_id,name.
"""

from os import getenv
from urllib.parse import urljoin
from dotenv import load_dotenv

from flask import request
from flask_restful import Resource

from project.models.course import Course
from project.utils.query_agent import query_selected_from_model, insert_into_model
from project.utils.authentication import login_required, authorize_teacher
from project.endpoints.courses.courses_utils import check_data

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(f"{API_URL}/", "courses")

class CourseForUser(Resource):
    """Api endpoint for the /courses link"""

    @login_required
    def get(self):
        """ "
        Get function for /courses this will be the main endpoint
        to get all courses and filter by given query parameter like /courses?parameter=...
        parameters can be either one of the following: teacher,ufora_id,name.
        """

        return query_selected_from_model(
            Course,
            RESPONSE_URL,
            url_mapper={"course_id": RESPONSE_URL},
            filters=request.args
        )

    @authorize_teacher
    def post(self, teacher_id=None):
        """
        This function will create a new course
        if the body of the post contains a name and uid is an admin or teacher
        """

        message, status = check_data(request.json, False)
        if status != 200:
            return message, status

        req = request.json
        req["teacher"] = teacher_id
        return insert_into_model(
            Course,
            req,
            RESPONSE_URL,
            "course_id",
            required_fields=["name", "teacher"]
        )
