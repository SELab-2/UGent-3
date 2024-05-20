"""
This file contains the main endpoint for the /courses url.
This endpoint is used to get all courses and filter by given
query parameter like /courses?parameter=...
parameters can be either one of the following: teacher,ufora_id,name.
"""

from os import getenv
from urllib.parse import urljoin
from dataclasses import fields
from dotenv import load_dotenv

from flask import request
from flask_restful import Resource

from sqlalchemy import union, select
from sqlalchemy.exc import SQLAlchemyError

from project.models.course import Course
from project.models.course_relation import CourseAdmin, CourseStudent
from project.utils.query_agent import insert_into_model
from project.utils.authentication import login_required_return_uid, authorize_teacher
from project.endpoints.courses.courses_utils import check_data
from project.db_in import db

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(f"{API_URL}/", "courses")

class CourseForUser(Resource):
    """Api endpoint for the /courses link"""

    @login_required_return_uid
    def get(self, uid=None):
        """ "
        Get function for /courses this will be the main endpoint
        to get all courses and filter by given query parameter like /courses?parameter=...
        parameters can be either one of the following: teacher,ufora_id,name.
        """

        try:
            filter_params = {
                key: value for key, value
                in request.args.to_dict().items()
                if key in {f.name for f in fields(Course)}
            }

            # Start with a base query
            base_query = select(Course)

            # Apply filters dynamically if they are provided
            for param, value in filter_params.items():
                if value:
                    if param in Course.__table__.columns:
                        attribute = getattr(Course, param)
                        base_query = base_query.filter(attribute == value)

            # Define the role-specific queries
            student_courses = base_query.join(
                CourseStudent,
                Course.course_id == CourseStudent.course_id).filter(
                    CourseStudent.uid == uid)
            admin_courses = base_query.join(
                CourseAdmin,
                Course.course_id == CourseAdmin.course_id).filter(
                    CourseAdmin.uid == uid)
            teacher_courses = base_query.filter(Course.teacher == uid)

            # Combine the select statements using union to remove duplicates
            all_courses_query = union(student_courses, admin_courses, teacher_courses)

            # Execute the union query and fetch all results as Course instances
            courses = db.session.execute(all_courses_query).mappings().all()
            courses_data = [dict(course) for course in courses]

            for course in courses_data:
                course["course_id"] = urljoin(f"{RESPONSE_URL}/", str(course['course_id']))

            return {
                "data": courses_data,
                "url": RESPONSE_URL,
                "message": "Courses fetched successfully"
            }

        except SQLAlchemyError:
            db.session.rollback()
            return {
                "message": "An error occurred while fetching the courses",
                "url": RESPONSE_URL
                }, 500

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
