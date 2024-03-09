"""
This file contains the api endpoint for the /courses/course_id url
This file is responsible for handling the requests made to the /courses/course_id url
and returning the appropriate response as well as handling the requests made to the
/courses/course_id/admins and /courses/course_id/students urls
"""

from os import getenv
from urllib.parse import urljoin

from dotenv import load_dotenv

from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from project.models.courses import Course
from project.models.course_relations import CourseAdmin, CourseStudent

from project import db
from project.utils.query_agent import delete_by_id_from_model, patch_by_id_from_model

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(API_URL + "/", "courses")

class CourseByCourseId(Resource):
    """Api endpoint for the /courses/course_id link"""

    def get(self, course_id):
        """
        This get function will return all the related projects of the course
        in the following form:
        {
            course: course with course_id
            projects: [
                list of all projects that have course_id
                where projects are jsons containing the title, deadline and project_id
            ]
        }
        """
        try:
            course_details = db.session.query(
                Course.course_id,
                Course.name,
                Course.ufora_id,
                Course.teacher
                ).filter(
                    Course.course_id == course_id).first()

            if not course_details:
                return {
                    "message": "Course not found",
                    "url": RESPONSE_URL
                }, 404

            admins = db.session.query(CourseAdmin.uid).filter(
                CourseAdmin.course_id == course_id
            ).all()

            students = db.session.query(CourseStudent.uid).filter(
                CourseStudent.course_id == course_id
            ).all()

            user_url = urljoin(API_URL + "/", "users")

            admin_ids = [ urljoin(f"{user_url}/" , admin[0]) for admin in admins]
            student_ids = [ urljoin(f"{user_url}/", student[0])  for student in students]

            result = {
                'course_id': course_details.course_id,
                'name': course_details.name,
                'ufora_id': course_details.ufora_id,
                'teacher': course_details.teacher,
                'admins': admin_ids,
                'students': student_ids
            }

            return {
                "message": f"Succesfully retrieved course with course_id: {str(course_id)}",
                "data": result,
                "url": urljoin(f"{RESPONSE_URL}/", str(course_id))
            }
        except SQLAlchemyError:
            return {
                "error": "Something went wrong while querying the database.",
                "url": RESPONSE_URL}, 500

    def delete(self, course_id):
        """
        This function will delete the course with course_id
        """
        return delete_by_id_from_model(
            Course,
            "course_id",
            course_id,
            RESPONSE_URL
        )

    def patch(self, course_id):
        """
        This function will update the course with course_id
        """

        return patch_by_id_from_model(
            Course,
            "course_id",
            course_id,
            RESPONSE_URL,
            request.json
        )
